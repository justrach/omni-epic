import numpy as np
from oped.envs.r2d2.base import R2D2Env

class Env(R2D2Env):
    """
    Kick ball through moving gates to zones marked by moving targets.

    The environment consists of a large flat ground. A ball is placed 5 meters directly in front of the robot. After a delay of 1-2 seconds (randomized), the ball begins rolling straight ahead at a constant velocity of 1-2 m/s (randomized).

    Five vertical rectangular gates, each 3 meters tall and 1 meter wide, are placed at randomized positions between 5 to 25 meters in front of the ball's initial position, at randomized lateral offsets up to 5 meters on either side. The gates translate laterally with randomized constant velocities between 0.2-1 m/s, reversing direction each time they move 5 meters from their initial position. The gates' movement is triggered at the start of the episode.

    Five target zones are marked on the ground at randomized positions between 10 to 30 meters in front of the ball's initial position, at randomized lateral offsets up to 10 meters on either side. Each target zone is a circle with radius 2 meters. At the center of each target zone is a flat cylindrical marker, 2 meters in radius and 0.1 meters tall. The markers rotate in place with randomized constant angular velocities between 0.1-0.5 rad/s, switching between clockwise and counterclockwise rotation each time the ball passes through a gate. The markers' rotation is triggered at the start of the episode.

    The robot is initialized 3 meters behind the ball, facing the direction of the ball's initial velocity.

    The task is for the robot to kick the ball through each gate in order, aiming to get the ball to stop within the corresponding target zone after it passes through the gate. The robot should decide when and how to kick the ball based on the observed motion of the gates and markers.

    Passing through a gate awards 2 points if the ball subsequently stops in the correct target zone, and 1 point otherwise. The episode ends when the ball passes through all gates, or a maximum time limit is reached. The robot should aim to maximize its total score.
    """

    def __init__(self):
        super().__init__()
        self.ground_size = [100.0, 100.0, 0.1]
        self.ground_position = [0.0, 0.0, 0.0]
        self.ground_id = self.create_box(mass=0.0, half_extents=[self.ground_size[0] / 2, self.ground_size[1] / 2, self.ground_size[2] / 2], position=self.ground_position, color=[0.5, 0.5, 0.5, 1.0])
        self._p.changeDynamics(bodyUniqueId=self.ground_id, linkIndex=-1, lateralFriction=0.8, restitution=0.5)
        self.ball_radius = 0.5
        self.ball_position_init = [0.0, 0.0, self.ground_size[2] / 2 + self.ball_radius]
        self.ball_id = self.create_sphere(mass=1.0, radius=self.ball_radius, position=self.ball_position_init, color=[1.0, 0.0, 0.0, 1.0])
        self.num_gates = 5
        self.gate_width = 1.0
        self.gate_height = 3.0
        self.gate_thickness = 0.1
        self.gate_ids = []
        self.gate_positions_init = []
        self.gate_velocities = []
        for _ in range(self.num_gates):
            gate_x = np.random.uniform(5.0, 25.0)
            gate_y = np.random.uniform(-5.0, 5.0)
            gate_position_init = [gate_x, gate_y, self.ground_size[2] / 2 + self.gate_height / 2]
            self.gate_positions_init.append(gate_position_init)
            gate_left_id = self.create_box(mass=0.0, half_extents=[self.gate_thickness / 2, self.gate_width / 2, self.gate_height / 2], position=[gate_position_init[0], gate_position_init[1] - self.gate_width / 2, gate_position_init[2]], color=[0.0, 0.0, 1.0, 1.0])
            gate_right_id = self.create_box(mass=0.0, half_extents=[self.gate_thickness / 2, self.gate_width / 2, self.gate_height / 2], position=[gate_position_init[0], gate_position_init[1] + self.gate_width / 2, gate_position_init[2]], color=[0.0, 0.0, 1.0, 1.0])
            self.gate_ids.append((gate_left_id, gate_right_id))
            gate_velocity = np.random.uniform(0.2, 1.0) * np.random.choice([-1.0, 1.0])
            self.gate_velocities.append(gate_velocity)
        self.num_targets = 5
        self.target_radius = 2.0
        self.target_height = 0.1
        self.target_ids = []
        self.target_positions_init = []
        self.target_angular_velocities = []
        for _ in range(self.num_targets):
            target_x = np.random.uniform(10.0, 30.0)
            target_y = np.random.uniform(-10.0, 10.0)
            target_position_init = [target_x, target_y, self.ground_size[2] / 2 + self.target_height / 2]
            self.target_positions_init.append(target_position_init)
            target_id = self.create_cylinder(mass=0.0, radius=self.target_radius, height=self.target_height, position=target_position_init, color=[0.0, 1.0, 0.0, 1.0])
            self.target_ids.append(target_id)
            target_angular_velocity = np.random.uniform(0.1, 0.5) * np.random.choice([-1.0, 1.0])
            self.target_angular_velocities.append(target_angular_velocity)
        self.robot_position_init = [self.ball_position_init[0] - 3.0, self.ball_position_init[1], self.ground_size[2] / 2 + self.robot.links['base'].position_init[2]]
        self.robot_orientation_init = self._p.getQuaternionFromEuler([0.0, 0.0, 0.0])
        self.max_steps = 2000
        self.gate_counter = 0
        self.score = 0

    def create_box(self, mass, half_extents, position, color):
        collision_shape_id = self._p.createCollisionShape(shapeType=self._p.GEOM_BOX, halfExtents=half_extents)
        visual_shape_id = self._p.createVisualShape(shapeType=self._p.GEOM_BOX, halfExtents=half_extents, rgbaColor=color)
        return self._p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_shape_id, baseVisualShapeIndex=visual_shape_id, basePosition=position)

    def create_sphere(self, mass, radius, position, color):
        collision_shape_id = self._p.createCollisionShape(shapeType=self._p.GEOM_SPHERE, radius=radius)
        visual_shape_id = self._p.createVisualShape(shapeType=self._p.GEOM_SPHERE, radius=radius, rgbaColor=color)
        return self._p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_shape_id, baseVisualShapeIndex=visual_shape_id, basePosition=position)

    def create_cylinder(self, mass, radius, height, position, color):
        collision_shape_id = self._p.createCollisionShape(shapeType=self._p.GEOM_CYLINDER, radius=radius, height=height)
        visual_shape_id = self._p.createVisualShape(shapeType=self._p.GEOM_CYLINDER, radius=radius, length=height, rgbaColor=color)
        return self._p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_shape_id, baseVisualShapeIndex=visual_shape_id, basePosition=position)

    def get_object_position(self, object_id):
        return np.asarray(self._p.getBasePositionAndOrientation(object_id)[0])

    def get_object_velocity(self, object_id):
        return np.asarray(self._p.getBaseVelocity(object_id)[0])

    def reset(self):
        observation = super().reset()
        self.ball_velocity_init = [np.random.uniform(1.0, 2.0), 0.0, 0.0]
        self.ball_delay = np.random.uniform(1.0, 2.0)
        self._p.resetBasePositionAndOrientation(self.ball_id, self.ball_position_init, [0.0, 0.0, 0.0, 1.0])
        self._p.resetBaseVelocity(self.ball_id, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        for i, (gate_left_id, gate_right_id) in enumerate(self.gate_ids):
            gate_position_init = self.gate_positions_init[i]
            self._p.resetBasePositionAndOrientation(gate_left_id, [gate_position_init[0], gate_position_init[1] - self.gate_width / 2, gate_position_init[2]], [0.0, 0.0, 0.0, 1.0])
            self._p.resetBasePositionAndOrientation(gate_right_id, [gate_position_init[0], gate_position_init[1] + self.gate_width / 2, gate_position_init[2]], [0.0, 0.0, 0.0, 1.0])
        for i, target_id in enumerate(self.target_ids):
            target_position_init = self.target_positions_init[i]
            self._p.resetBasePositionAndOrientation(target_id, target_position_init, [0.0, 0.0, 0.0, 1.0])
        self._p.resetBasePositionAndOrientation(self.robot.robot_id, self.robot_position_init, self.robot_orientation_init)
        self.time = 0.0
        self.steps = 0
        self.gate_counter = 0
        self.score = 0
        return observation

    def step(self, action):
        self.ball_position = self.get_object_position(self.ball_id)
        self.ball_velocity = self.get_object_velocity(self.ball_id)
        observation, reward, terminated, truncated, info = super().step(action)
        self.time += self.dt
        self.steps += 1
        if self.time > self.ball_delay:
            self._p.resetBaseVelocity(self.ball_id, self.ball_velocity_init, [0.0, 0.0, 0.0])
        for i, (gate_left_id, gate_right_id) in enumerate(self.gate_ids):
            gate_position = self.get_object_position(gate_left_id)
            gate_velocity = self.gate_velocities[i]
            if abs(gate_position[1] - self.gate_positions_init[i][1]) > 5.0:
                gate_velocity *= -1.0
                self.gate_velocities[i] = gate_velocity
            new_gate_position = [gate_position[0], gate_position[1] + gate_velocity * self.dt, gate_position[2]]
            self._p.resetBasePositionAndOrientation(gate_left_id, [new_gate_position[0], new_gate_position[1] - self.gate_width / 2, new_gate_position[2]], [0.0, 0.0, 0.0, 1.0])
            self._p.resetBasePositionAndOrientation(gate_right_id, [new_gate_position[0], new_gate_position[1] + self.gate_width / 2, new_gate_position[2]], [0.0, 0.0, 0.0, 1.0])
        for i, target_id in enumerate(self.target_ids):
            target_position = self.get_object_position(target_id)
            target_angular_velocity = self.target_angular_velocities[i]
            target_orientation = self._p.getQuaternionFromEuler([0.0, 0.0, target_angular_velocity * self.time])
            self._p.resetBasePositionAndOrientation(target_id, target_position, target_orientation)
        return (observation, reward, terminated, truncated, info)

    def get_task_rewards(self, action):
        gate_reward = 0.0
        if self.gate_counter < self.num_gates:
            gate_left_id, gate_right_id = self.gate_ids[self.gate_counter]
            if len(self._p.getContactPoints(bodyA=self.ball_id, bodyB=gate_left_id)) > 0 or len(self._p.getContactPoints(bodyA=self.ball_id, bodyB=gate_right_id)) > 0:
                self.gate_counter += 1
                if self.gate_counter < self.num_targets:
                    target_id = self.target_ids[self.gate_counter - 1]
                    if np.linalg.norm(self.get_object_position(self.ball_id)[:2] - self.get_object_position(target_id)[:2]) < self.target_radius:
                        gate_reward = 2.0
                    else:
                        gate_reward = 1.0
                    self.target_angular_velocities[self.gate_counter - 1] *= -1.0
                else:
                    gate_reward = 1.0
        self.score += gate_reward
        return {'gate_reward': gate_reward}

    def get_terminated(self, action):
        all_gates_passed = self.gate_counter >= self.num_gates
        time_limit_reached = self.steps >= self.max_steps
        return all_gates_passed or time_limit_reached

    def get_success(self):
        return self.gate_counter >= self.num_gates