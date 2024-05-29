import numpy as np
from oped.envs.r2d2.base import R2D2Env

class Env(R2D2Env):
    """
    Busy Restaurant Table Service

    Description: 
    - The environment is a busy restaurant dining area, consisting of a 12 m x 12 m room with 4 tables, an entrance door, and a kitchen door.
    - Restaurant patrons (simulated as cylinders) continuously enter from the entrance, move to a table, stay for a period of time, and then exit, making the environment dynamic.
    - The robot must perform two types of table service tasks:
      1) Table setting: The robot must collect clean dishes and utensils from the kitchen and arrange them properly on the tables in preparation for new patrons. Dishes should be stacked neatly.
      2) Table busing: After patrons leave, the robot must clear dirty dishes and utensils from the tables, load them into a bin, and return the bin to the kitchen. The bin has a maximum capacity that the robot must respect.
    - The robot must avoid colliding with patrons and restaurant furniture as it navigates.
    - Dishes will break if dropped. The robot must handle them carefully.

    Success Conditions:
    - For table setting, success means all necessary dishes and utensils are properly placed on empty tables prior to new patrons arriving. Dishes should be undamaged and neatly stacked.
    - For table busing, success involves clearing all dirty dishes from unoccupied tables, loading them into the bin without exceeding capacity, and delivering the bin to the kitchen. No dishes should be broken.
    - The robot should avoid any collisions with patrons or furniture throughout the episode.

    Time Limit:
    The episode lasts for 10 minutes of simulated time. The robot must continuously perform both table setting and busing tasks during this period as needed.

    Rewards:
    - Provide a moderate reward for each successful table set, with all dishes placed neatly and undamaged.
    - Provide a moderate reward for each successful table busing, with no broken dishes and the bin delivered to the kitchen.
    - Give a small reward for carefully handling dishes without breaking them.
    - Assign a substantial penalty for any collisions between the robot and patrons or furniture.
    - Assign a small penalty for dropping and breaking a dish.
    - Provide a small reward at each timestep for maintaining a tidy dining room, with no dirty dishes left on unoccupied tables.

    Termination:
    The episode ends if the robot crashes into a patron or furniture, or if the time limit is reached. The episode is considered successful if the robot consistently performs both table setting and busing throughout the full time period with no collisions or broken dishes.
    """

    def __init__(self):
        super().__init__()
        self.course_size = [20.0, 20.0, 10.0]
        self.course_position = [0.0, 0.0, 0.0]
        self.num_levels = 5
        self.level_height = self.course_size[2] / self.num_levels
        self.platform_size = [5.0, 5.0, 0.5]
        self.ramp_size = [5.0, 2.0, 1.0]
        self.gap_size = 2.0
        self.wall_size = [2.0, 0.2, 2.0]
        self.cylinder_radius = 0.5
        self.cylinder_height = 2.0
        self.target_object_size = [1.0, 1.0, 1.0]
        self.target_object_position_init = [0.0, 0.0, self.course_size[2] - self.level_height / 2 - self.target_object_size[2] / 2]
        self.target_object_id = self.create_box(mass=1.0, half_extents=[self.target_object_size[0] / 2, self.target_object_size[1] / 2, self.target_object_size[2] / 2], position=self.target_object_position_init, color=[1.0, 0.0, 0.0, 1.0])
        self.goal_size = [2.0, 2.0, 0.01]
        self.goal_position = [self.course_size[0] / 2 - self.goal_size[0] / 2, 0.0, self.course_size[2] / 2 - self.level_height / 2 - self.goal_size[2] / 2]
        self.goal_id = self.create_box(mass=0.0, half_extents=[self.goal_size[0] / 2, self.goal_size[1] / 2, self.goal_size[2] / 2], position=self.goal_position, color=[0.0, 1.0, 0.0, 1.0])
        self.time_limit = 300.0
        self.platform_ids = []
        self.ramp_ids = []
        self.wall_ids = []
        self.cylinder_ids = []
        self.create_course()
        self.robot_position_init = [-self.course_size[0] / 2 + 1.0, 0.0, self.course_size[2] / 2 - self.level_height / 2 + self.robot.links['base'].position_init[2]]

    def create_box(self, mass, half_extents, position, color):
        collision_shape_id = self._p.createCollisionShape(shapeType=self._p.GEOM_BOX, halfExtents=half_extents)
        visual_shape_id = self._p.createVisualShape(shapeType=self._p.GEOM_BOX, halfExtents=half_extents, rgbaColor=color)
        return self._p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_shape_id, baseVisualShapeIndex=visual_shape_id, basePosition=position)

    def create_cylinder(self, mass, radius, height, position, color):
        collision_shape_id = self._p.createCollisionShape(shapeType=self._p.GEOM_CYLINDER, radius=radius, height=height)
        visual_shape_id = self._p.createVisualShape(shapeType=self._p.GEOM_CYLINDER, radius=radius, length=height, rgbaColor=color)
        return self._p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_shape_id, baseVisualShapeIndex=visual_shape_id, basePosition=position)

    def create_course(self):
        for i in range(self.num_levels):
            level_position = [0.0, 0.0, self.course_size[2] / 2 - self.level_height * (i + 0.5)]
            platform_position = [level_position[0] + (i - self.num_levels / 2 + 0.5) * 5.0, level_position[1], level_position[2]]
            platform_id = self.create_box(mass=0.0, half_extents=[self.platform_size[0] / 2, self.platform_size[1] / 2, self.platform_size[2] / 2], position=platform_position, color=[0.5, 0.5, 0.5, 1.0])
            self.platform_ids.append(platform_id)
            if i < self.num_levels - 1:
                ramp_position = [platform_position[0] + self.platform_size[0] / 2 + self.ramp_size[0] / 2, platform_position[1], platform_position[2] + self.level_height / 2 - self.ramp_size[2] / 2]
                ramp_id = self.create_box(mass=0.0, half_extents=[self.ramp_size[0] / 2, self.ramp_size[1] / 2, self.ramp_size[2] / 2], position=ramp_position, color=[0.6, 0.4, 0.2, 1.0])
                self.ramp_ids.append(ramp_id)
            if i > 0:
                gap_position = [platform_position[0] - self.platform_size[0] / 2 - self.gap_size / 2, platform_position[1], platform_position[2]]
                wall_position_left = [gap_position[0] - self.gap_size / 2 - self.wall_size[0] / 2, gap_position[1] - self.platform_size[1] / 2 - self.wall_size[1] / 2, gap_position[2] + self.wall_size[2] / 2]
                wall_position_right = [gap_position[0] - self.gap_size / 2 - self.wall_size[0] / 2, gap_position[1] + self.platform_size[1] / 2 + self.wall_size[1] / 2, gap_position[2] + self.wall_size[2] / 2]
                wall_id_left = self.create_box(mass=0.0, half_extents=[self.wall_size[0] / 2, self.wall_size[1] / 2, self.wall_size[2] / 2], position=wall_position_left, color=[0.2, 0.2, 0.2, 1.0])
                wall_id_right = self.create_box(mass=0.0, half_extents=[self.wall_size[0] / 2, self.wall_size[1] / 2, self.wall_size[2] / 2], position=wall_position_right, color=[0.2, 0.2, 0.2, 1.0])
                self.wall_ids.append(wall_id_left)
                self.wall_ids.append(wall_id_right)
            if i < self.num_levels - 1:
                cylinder_position = [platform_position[0], platform_position[1] - self.platform_size[1] / 4, platform_position[2] + self.level_height / 2 - self.cylinder_height / 2]
                cylinder_id = self.create_cylinder(mass=0.0, radius=self.cylinder_radius, height=self.cylinder_height, position=cylinder_position, color=[0.8, 0.8, 0.8, 1.0])
                self.cylinder_ids.append(cylinder_id)

    def get_object_position(self, object_id):
        return np.asarray(self._p.getBasePositionAndOrientation(object_id)[0])

    def get_distance_to_object(self, object_id):
        object_position = self.get_object_position(object_id)
        robot_position = self.robot.links['base'].position
        return np.linalg.norm(object_position[:2] - robot_position[:2])

    def reset(self):
        observation = super().reset()
        self.time = 0.0
        self._p.resetBasePositionAndOrientation(self.target_object_id, self.target_object_position_init, [0.0, 0.0, 0.0, 1.0])
        self._p.resetBasePositionAndOrientation(self.robot.robot_id, self.robot_position_init, self.robot.links['base'].orientation_init)
        return observation

    def step(self, action):
        self.robot_position = self.robot.links['base'].position
        self.target_object_position = self.get_object_position(self.target_object_id)
        self.distance_to_target_object = self.get_distance_to_object(self.target_object_id)
        observation, reward, terminated, truncated, info = super().step(action)
        self.time += self.dt
        return (observation, reward, terminated, truncated, info)

    def get_task_rewards(self, action):
        new_robot_position = self.robot.links['base'].position
        new_target_object_position = self.get_object_position(self.target_object_id)
        new_distance_to_target_object = self.get_distance_to_object(self.target_object_id)
        forward_progression = (new_robot_position[0] - self.robot_position[0]) / self.dt
        elevation_scale = new_robot_position[2] / self.course_size[2]
        forward_progression_reward = 0.1 * forward_progression * elevation_scale
        reached_target_object_reward = 0.0
        if new_distance_to_target_object < 1.0 and self.distance_to_target_object >= 1.0:
            reached_target_object_reward = 10.0
        target_object_in_goal_reward = 0.0
        if self.goal_position[0] - self.goal_size[0] / 2 < new_target_object_position[0] < self.goal_position[0] + self.goal_size[0] / 2 and self.goal_position[1] - self.goal_size[1] / 2 < new_target_object_position[1] < self.goal_position[1] + self.goal_size[1] / 2:
            target_object_in_goal_reward = 100.0
        collision_penalty = 0.0
        for object_id in self.wall_ids + self.cylinder_ids:
            if len(self._p.getContactPoints(bodyA=self.robot.robot_id, bodyB=object_id)) > 0:
                collision_penalty -= 1.0
        return {'forward_progression_reward': forward_progression_reward, 'reached_target_object_reward': reached_target_object_reward, 'target_object_in_goal_reward': target_object_in_goal_reward, 'collision_penalty': collision_penalty}

    def get_terminated(self, action):
        robot_position = self.robot.links['base'].position
        if robot_position[2] < self.course_size[2] / 2 - self.level_height:
            return True
        if np.dot(np.asarray([0, 0, 1]), np.asarray(self._p.getMatrixFromQuaternion(self.robot.links['base'].orientation)).reshape(3, 3)[:, 2]) < 0.5:
            return True
        if self.time >= self.time_limit:
            return True
        return False

    def get_success(self):
        target_object_position = self.get_object_position(self.target_object_id)
        robot_position = self.robot.links['base'].position
        target_object_velocity = np.linalg.norm(self._p.getBaseVelocity(self.target_object_id)[0])
        is_target_object_in_goal = self.goal_position[0] - self.goal_size[0] / 2 < target_object_position[0] < self.goal_position[0] + self.goal_size[0] / 2 and self.goal_position[1] - self.goal_size[1] / 2 < target_object_position[1] < self.goal_position[1] + self.goal_size[1] / 2
        is_robot_in_goal = self.goal_position[0] - self.goal_size[0] / 2 < robot_position[0] < self.goal_position[0] + self.goal_size[0] / 2 and self.goal_position[1] - self.goal_size[1] / 2 < robot_position[1] < self.goal_position[1] + self.goal_size[1] / 2
        return is_target_object_in_goal and is_robot_in_goal and (target_object_velocity < 0.1)