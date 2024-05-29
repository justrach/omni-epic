import numpy as np
from oped.envs.r2d2.base import R2D2Env

class Env(R2D2Env):
    """
    Outdoor Retrieval Challenge

    Description:
    - The environment is a large outdoor field 50 m x 50 m, with the robot starting in the center. 
    - The terrain includes various features:
      - A steep hill with a 30 degree incline
      - A shallow stream, 0.5 m deep and 5 m wide
      - Patches of loose sand and gravel
      - Scattered trees and boulders up to 2 m tall
    - A 0.5 m diameter soccer ball is placed randomly between 10 m and 20 m from the robot's starting position.
    - The robot must locate the ball, pick it up or get it balanced on its back, and return it to the starting location.
    - The ball is heavy enough that it can't simply be pushed the whole way. The robot needs to lift/carry it.
    - If the robot drops the ball or it rolls more than 5 m away, it is replaced at a new random location.

    Success Conditions:
    The task is completed when the robot returns to within 2 m of its starting position with the ball balanced on its back or in its possession.

    Time Limit:
    The robot has 10 minutes to complete the retrieval.

    Rewards:
    - Provide a small reward for exploring the environment and locating the ball
    - Provide a moderate reward for successfully getting the ball balanced on the robot's back or lifted off the ground 
    - Provide a large reward for returning to the start area with the ball
    - Provide a small penalty if the ball is dropped or lost, to encourage careful handling

    Termination:
    The episode ends if the robot flips over and can't right itself, or if the time limit is exceeded.
    """

    def __init__(self):
        super().__init__()
        self.field_size = [50.0, 50.0, 0.0]
        self.robot_start_position = [0.0, 0.0, 0.0]
        self.ground_thickness = 0.2
        self.ground_id = self.create_box(mass=0.0, half_extents=[self.field_size[0] / 2, self.field_size[1] / 2, self.ground_thickness / 2], position=[0.0, 0.0, -self.ground_thickness / 2], orientation=[0.0, 0.0, 0.0, 1.0], color=[0.5, 0.5, 0.5, 1.0])
        self._p.changeDynamics(bodyUniqueId=self.ground_id, linkIndex=-1, lateralFriction=0.8, restitution=0.2)
        self.ball_radius = 0.25
        self.ball_mass = 1.0
        self.ball_start_distance_range = [10.0, 20.0]
        self.ball_start_position = self.get_random_ball_start_position()
        self.ball_id = self.create_sphere(mass=self.ball_mass, radius=self.ball_radius, position=self.ball_start_position, color=[1.0, 1.0, 1.0, 1.0])
        self.ball_lost_distance = 5.0
        self.success_distance = 2.0
        self.time_limit = 600.0
        self.terrain_ids = []
        self.create_terrain()

    def create_sphere(self, mass, radius, position, color):
        collision_shape_id = self._p.createCollisionShape(shapeType=self._p.GEOM_SPHERE, radius=radius)
        visual_shape_id = self._p.createVisualShape(shapeType=self._p.GEOM_SPHERE, radius=radius, rgbaColor=color)
        return self._p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_shape_id, baseVisualShapeIndex=visual_shape_id, basePosition=position)

    def create_box(self, mass, half_extents, position, orientation, color):
        collision_shape_id = self._p.createCollisionShape(shapeType=self._p.GEOM_BOX, halfExtents=half_extents)
        visual_shape_id = self._p.createVisualShape(shapeType=self._p.GEOM_BOX, halfExtents=half_extents, rgbaColor=color)
        return self._p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_shape_id, baseVisualShapeIndex=visual_shape_id, basePosition=position, baseOrientation=orientation)

    def create_cylinder(self, mass, radius, height, position, orientation, color):
        collision_shape_id = self._p.createCollisionShape(shapeType=self._p.GEOM_CYLINDER, radius=radius, height=height)
        visual_shape_id = self._p.createVisualShape(shapeType=self._p.GEOM_CYLINDER, radius=radius, length=height, rgbaColor=color)
        return self._p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_shape_id, baseVisualShapeIndex=visual_shape_id, basePosition=position, baseOrientation=orientation)

    def create_terrain(self):
        hill_height = 5.0
        hill_half_extents = [10.0, 10.0, hill_height / 2]
        hill_position = [15.0, 15.0, hill_height / 2]
        hill_orientation = self._p.getQuaternionFromEuler([0.0, 0.0, np.random.uniform(0.0, 2 * np.pi)])
        hill_id = self.create_box(mass=0.0, half_extents=hill_half_extents, position=hill_position, orientation=hill_orientation, color=[0.5, 0.5, 0.5, 1.0])
        self.terrain_ids.append(hill_id)
        stream_depth = 0.5
        stream_half_extents = [2.5, 25.0, stream_depth / 2]
        stream_position = [-15.0, 0.0, stream_depth / 2]
        stream_orientation = self._p.getQuaternionFromEuler([0.0, 0.0, 0.0])
        stream_id = self.create_box(mass=0.0, half_extents=stream_half_extents, position=stream_position, orientation=stream_orientation, color=[0.0, 0.0, 1.0, 0.5])
        self.terrain_ids.append(stream_id)
        num_patches = 10
        patch_radius = 3.0
        for _ in range(num_patches):
            patch_position = [np.random.uniform(-25.0, 25.0), np.random.uniform(-25.0, 25.0), 0.05]
            patch_orientation = self._p.getQuaternionFromEuler([0.0, 0.0, np.random.uniform(0.0, 2 * np.pi)])
            patch_id = self.create_cylinder(mass=0.0, radius=patch_radius, height=0.1, position=patch_position, orientation=patch_orientation, color=[0.8, 0.8, 0.4, 1.0])
            self.terrain_ids.append(patch_id)
        num_obstacles = 20
        obstacle_radius_range = [0.5, 1.0]
        obstacle_height_range = [1.0, 2.0]
        for _ in range(num_obstacles):
            obstacle_radius = np.random.uniform(obstacle_radius_range[0], obstacle_radius_range[1])
            obstacle_height = np.random.uniform(obstacle_height_range[0], obstacle_height_range[1])
            obstacle_position = [np.random.uniform(-25.0, 25.0), np.random.uniform(-25.0, 25.0), obstacle_height / 2]
            obstacle_orientation = self._p.getQuaternionFromEuler([0.0, 0.0, np.random.uniform(0.0, 2 * np.pi)])
            if np.random.rand() < 0.5:
                obstacle_id = self.create_cylinder(mass=0.0, radius=obstacle_radius, height=obstacle_height, position=obstacle_position, orientation=obstacle_orientation, color=[0.4, 0.2, 0.0, 1.0])
            else:
                obstacle_id = self.create_box(mass=0.0, half_extents=[obstacle_radius, obstacle_radius, obstacle_height / 2], position=obstacle_position, orientation=obstacle_orientation, color=[0.5, 0.5, 0.5, 1.0])
            self.terrain_ids.append(obstacle_id)

    def get_random_ball_start_position(self):
        angle = np.random.uniform(0.0, 2 * np.pi)
        distance = np.random.uniform(self.ball_start_distance_range[0], self.ball_start_distance_range[1])
        x = self.robot_start_position[0] + distance * np.cos(angle)
        y = self.robot_start_position[1] + distance * np.sin(angle)
        z = self.ball_radius
        return [x, y, z]

    def get_object_position(self, object_id):
        return np.asarray(self._p.getBasePositionAndOrientation(object_id)[0])

    def get_distance_to_object(self, object_id):
        object_position = self.get_object_position(object_id)
        robot_position = self.robot.links['base'].position
        return np.linalg.norm(object_position[:2] - robot_position[:2])

    def reset(self):
        observation = super().reset()
        self.time = 0.0
        self.ball_start_position = self.get_random_ball_start_position()
        self._p.resetBasePositionAndOrientation(self.ball_id, self.ball_start_position, [0.0, 0.0, 0.0, 1.0])
        self._p.resetBasePositionAndOrientation(self.robot.robot_id, [self.robot_start_position[0], self.robot_start_position[1], self.ground_thickness / 2 + self.robot.links['base'].position_init[2]], self.robot.links['base'].orientation_init)
        return observation

    def step(self, action):
        self.ball_position = self.get_object_position(self.ball_id)
        self.robot_position = self.robot.links['base'].position
        self.distance_to_ball = self.get_distance_to_object(self.ball_id)
        observation, reward, terminated, truncated, info = super().step(action)
        self.time += self.dt
        if self.distance_to_ball > self.ball_lost_distance:
            self.ball_start_position = self.get_random_ball_start_position()
            self._p.resetBasePositionAndOrientation(self.ball_id, self.ball_start_position, [0.0, 0.0, 0.0, 1.0])
        return (observation, reward, terminated, truncated, info)

    def get_task_rewards(self, action):
        new_ball_position = self.get_object_position(self.ball_id)
        new_robot_position = self.robot.links['base'].position
        new_distance_to_ball = self.get_distance_to_object(self.ball_id)
        explore_reward = 0.1 * (self.distance_to_ball - new_distance_to_ball) / self.dt
        pickup_reward = 0.0
        if self._p.getContactPoints(bodyA=self.robot.robot_id, bodyB=self.ball_id) and new_ball_position[2] > self.ball_radius:
            pickup_reward = 10.0
        return_reward = 0.0
        if new_distance_to_ball < self.success_distance and np.linalg.norm(new_robot_position[:2] - self.robot_start_position[:2]) < self.success_distance:
            return_reward = 100.0
        drop_penalty = -1.0 if new_distance_to_ball > self.ball_lost_distance else 0.0
        return {'explore_reward': explore_reward, 'pickup_reward': pickup_reward, 'return_reward': return_reward, 'drop_penalty': drop_penalty}

    def get_terminated(self, action):
        if np.dot(np.asarray([0, 0, 1]), np.asarray(self._p.getMatrixFromQuaternion(self.robot.links['base'].orientation)).reshape(3, 3)[:, 2]) < 0.5:
            return True
        if self.time >= self.time_limit:
            return True
        return False

    def get_success(self):
        ball_position = self.get_object_position(self.ball_id)
        robot_position = self.robot.links['base'].position
        distance_to_ball = self.get_distance_to_object(self.ball_id)
        return distance_to_ball < self.success_distance and np.linalg.norm(robot_position[:2] - self.robot_start_position[:2]) < self.success_distance and (ball_position[2] > self.ball_radius)