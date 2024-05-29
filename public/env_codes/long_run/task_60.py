import numpy as np
from oped.envs.r2d2.base import R2D2Env

class Env(R2D2Env):
    """
    Simplified 1-vs-1 robot soccer.

    Description:
    - The environment consists of a large flat ground representing a soccer field.
    - Two goals are placed on opposite ends of the field, each defined by two posts 2 meters high and 3 meters apart.  
    - The robot is placed on one side of the field, facing the opponent's goal.
    - A basic opponent robot is placed on the other side, initially stationary.
    - A soccer ball is placed in the center of the field.
    - The objective is for the robot to navigate to the ball, take possession of it, and kick it into the opponent's goal while defending its own goal.
    - In the first stage, the opponent robot remains stationary. In the second stage, the opponent robot also moves to chase after the ball and attempt to kick it into the robot's goal.

    Success:
    The task is completed successfully if the robot is able to kick the ball into the opponent's goal while preventing the opponent from scoring.

    Rewards:
    - The robot is rewarded for possessing the ball, defined as being within 1 meter of the ball while the opponent is not.
    - The robot is rewarded for bringing the ball closer to the opponent's goal.
    - The robot is rewarded for kicking the ball with a velocity toward the opponent's goal.
    - The robot is penalized if the opponent takes possession of the ball or if the ball goes out of bounds.
    - The robot is greatly rewarded for scoring a goal and penalized if the opponent scores.

    Termination:
    The task is terminated if a goal is scored by either side, if the ball goes out of bounds, or if a time limit is reached.
    """

    def __init__(self):
        super().__init__()
        self.field_size = [40.0, 20.0, 10.0]
        self.field_position = [0.0, 0.0, 0.0]
        self.field_id = self.create_box(mass=0.0, half_extents=[self.field_size[0] / 2, self.field_size[1] / 2, self.field_size[2] / 2], position=self.field_position, color=[0.0, 0.5, 0.0, 1.0])
        self._p.changeDynamics(bodyUniqueId=self.field_id, linkIndex=-1, lateralFriction=0.8, restitution=0.5)
        self.ball_radius = 0.5
        self.ball_position_init = [0.0, 0.0, self.field_size[2] / 2 + self.ball_radius]
        self.ball_id = self.create_sphere(mass=1.0, radius=self.ball_radius, position=self.ball_position_init, color=[1.0, 1.0, 1.0, 1.0])
        self.goal_post_height = 2.0
        self.goal_post_radius = 0.1
        self.goal_width = 3.0
        self.goal_1_position = [self.field_size[0] / 2, 0.0, self.field_size[2] / 2 + self.goal_post_height / 2]
        self.goal_1_post_left_id = self.create_cylinder(mass=0.0, radius=self.goal_post_radius, height=self.goal_post_height, position=[self.goal_1_position[0], self.goal_1_position[1] - self.goal_width / 2, self.goal_1_position[2]], color=[1.0, 0.0, 0.0, 1.0])
        self.goal_1_post_right_id = self.create_cylinder(mass=0.0, radius=self.goal_post_radius, height=self.goal_post_height, position=[self.goal_1_position[0], self.goal_1_position[1] + self.goal_width / 2, self.goal_1_position[2]], color=[1.0, 0.0, 0.0, 1.0])
        self.goal_2_position = [-self.field_size[0] / 2, 0.0, self.field_size[2] / 2 + self.goal_post_height / 2]
        self.goal_2_post_left_id = self.create_cylinder(mass=0.0, radius=self.goal_post_radius, height=self.goal_post_height, position=[self.goal_2_position[0], self.goal_2_position[1] - self.goal_width / 2, self.goal_2_position[2]], color=[0.0, 0.0, 1.0, 1.0])
        self.goal_2_post_right_id = self.create_cylinder(mass=0.0, radius=self.goal_post_radius, height=self.goal_post_height, position=[self.goal_2_position[0], self.goal_2_position[1] + self.goal_width / 2, self.goal_2_position[2]], color=[0.0, 0.0, 1.0, 1.0])
        self.robot_position_init = [-self.field_size[0] / 4, 0.0, self.field_size[2] / 2 + self.robot.links['base'].position_init[2]]
        self.robot_orientation_init = self._p.getQuaternionFromEuler([0.0, 0.0, np.pi])
        self.opponent_position_init = [self.field_size[0] / 4, 0.0, self.field_size[2] / 2 + self.robot.links['base'].position_init[2]]
        self.opponent_orientation_init = self._p.getQuaternionFromEuler([0.0, 0.0, 0.0])
        self.opponent_id = self.create_opponent()
        self.possession_distance = 1.0
        self.max_steps = 1000

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

    def create_opponent(self):
        opponent_size = [0.5, 0.5, 1.0]
        opponent_id = self.create_box(mass=1.0, half_extents=[opponent_size[0] / 2, opponent_size[1] / 2, opponent_size[2] / 2], position=self.opponent_position_init, color=[0.0, 0.0, 0.0, 1.0])
        return opponent_id

    def get_object_position(self, object_id):
        return np.asarray(self._p.getBasePositionAndOrientation(object_id)[0])

    def get_object_velocity(self, object_id):
        return np.asarray(self._p.getBaseVelocity(object_id)[0])

    def get_distance_to_object(self, object_id):
        object_position = self.get_object_position(object_id)
        robot_position = self.robot.links['base'].position
        return np.linalg.norm(object_position[:2] - robot_position[:2])

    def reset(self):
        observation = super().reset()
        self._p.resetBasePositionAndOrientation(self.ball_id, self.ball_position_init, [0.0, 0.0, 0.0, 1.0])
        self._p.resetBaseVelocity(self.ball_id, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        self._p.resetBasePositionAndOrientation(self.robot.robot_id, self.robot_position_init, self.robot_orientation_init)
        self._p.resetBasePositionAndOrientation(self.opponent_id, self.opponent_position_init, self.opponent_orientation_init)
        self.steps = 0
        return observation

    def step(self, action):
        self.ball_position = self.get_object_position(self.ball_id)
        self.ball_velocity = self.get_object_velocity(self.ball_id)
        self.robot_position = self.robot.links['base'].position
        self.opponent_position = self.get_object_position(self.opponent_id)
        self.distance_to_ball = self.get_distance_to_object(self.ball_id)
        self.opponent_distance_to_ball = np.linalg.norm(self.opponent_position[:2] - self.ball_position[:2])
        observation, reward, terminated, truncated, info = super().step(action)
        self.steps += 1
        return (observation, reward, terminated, truncated, info)

    def get_task_rewards(self, action):
        new_ball_position = self.get_object_position(self.ball_id)
        new_ball_velocity = self.get_object_velocity(self.ball_id)
        new_robot_position = self.robot.links['base'].position
        new_opponent_position = self.get_object_position(self.opponent_id)
        new_distance_to_ball = self.get_distance_to_object(self.ball_id)
        new_opponent_distance_to_ball = np.linalg.norm(new_opponent_position[:2] - new_ball_position[:2])
        possession = 1.0 if new_distance_to_ball < self.possession_distance and new_opponent_distance_to_ball >= self.possession_distance else 0.0
        ball_progress = (self.ball_position[0] - new_ball_position[0]) / self.dt
        kick_velocity = 0.0
        if len(self._p.getContactPoints(bodyA=self.robot.robot_id, bodyB=self.ball_id)) > 0:
            kick_velocity = np.dot(new_ball_velocity, [1.0, 0.0, 0.0])
        opponent_possession = -1.0 if new_opponent_distance_to_ball < self.possession_distance and new_distance_to_ball >= self.possession_distance else 0.0
        ball_out_of_bounds = -1.0 if np.abs(new_ball_position[0]) > self.field_size[0] / 2 or np.abs(new_ball_position[1]) > self.field_size[1] / 2 else 0.0
        robot_goal = 10.0 if self.goal_1_position[1] - self.goal_width / 2 < new_ball_position[1] < self.goal_1_position[1] + self.goal_width / 2 and new_ball_position[0] > self.goal_1_position[0] else 0.0
        opponent_goal = -10.0 if self.goal_2_position[1] - self.goal_width / 2 < new_ball_position[1] < self.goal_2_position[1] + self.goal_width / 2 and new_ball_position[0] < self.goal_2_position[0] else 0.0
        return {'possession': possession, 'ball_progress': ball_progress, 'kick_velocity': kick_velocity, 'opponent_possession': opponent_possession, 'ball_out_of_bounds': ball_out_of_bounds, 'robot_goal': robot_goal, 'opponent_goal': opponent_goal}

    def get_terminated(self, action):
        ball_position = self.get_object_position(self.ball_id)
        robot_goal = self.goal_1_position[1] - self.goal_width / 2 < ball_position[1] < self.goal_1_position[1] + self.goal_width / 2 and ball_position[0] > self.goal_1_position[0]
        opponent_goal = self.goal_2_position[1] - self.goal_width / 2 < ball_position[1] < self.goal_2_position[1] + self.goal_width / 2 and ball_position[0] < self.goal_2_position[0]
        ball_out_of_bounds = np.abs(ball_position[0]) > self.field_size[0] / 2 or np.abs(ball_position[1]) > self.field_size[1] / 2
        time_limit_reached = self.steps >= self.max_steps
        return robot_goal or opponent_goal or ball_out_of_bounds or time_limit_reached

    def get_success(self):
        ball_position = self.get_object_position(self.ball_id)
        robot_goal = self.goal_1_position[1] - self.goal_width / 2 < ball_position[1] < self.goal_1_position[1] + self.goal_width / 2 and ball_position[0] > self.goal_1_position[0]
        opponent_goal = self.goal_2_position[1] - self.goal_width / 2 < ball_position[1] < self.goal_2_position[1] + self.goal_width / 2 and ball_position[0] < self.goal_2_position[0]
        return robot_goal and (not opponent_goal)