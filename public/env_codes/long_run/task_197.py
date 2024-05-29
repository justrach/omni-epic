import numpy as np
from oped.envs.r2d2.base import R2D2Env

class Env(R2D2Env):
    """
    Task: Jumping Over Gaps

    Description:
    - The environment consists of a 10 m x 10 m platform with a series of gaps that the robot must jump over.
    - The platform is divided into three sections:
      1. The first section (3 m x 10 m) has three gaps, each 0.5 m wide, spaced 2 m apart.
      2. The second section (3 m x 10 m) has two gaps, each 1 m wide, spaced 3 m apart.
      3. The third section (4 m x 10 m) has one gap, 1.5 m wide, located 2 m from the end of the platform.

    - The robot begins at the start of the platform, facing the positive x-axis.

    Task:
    The robot must navigate through the three sections of the platform, jumping over the gaps to reach the end of the platform.

    Success Conditions:
    The task is considered complete when the robot reaches the end of the platform without falling into any gaps.

    Rewards:
    - Provide a small reward for each gap successfully jumped over.
    - Provide a large reward for reaching the end of the platform.
    - Apply a small penalty for each failed jump (falling into a gap).

    Termination:
    The episode ends if the robot falls into a gap, flips over, or reaches the end of the platform.
    """

    def __init__(self):
        super().__init__()
        self.platform_size = [10.0, 10.0, 0.1]
        self.platform_position = [0.0, 0.0, 0.0]
        self.platform_id = self.create_box(mass=0.0, half_extents=[self.platform_size[0] / 2, self.platform_size[1] / 2, self.platform_size[2] / 2], position=self.platform_position, color=[0.5, 0.5, 0.5, 1.0])
        self._p.changeDynamics(bodyUniqueId=self.platform_id, linkIndex=-1, lateralFriction=0.8, restitution=0.5)
        self.gap_widths = [0.5, 0.5, 0.5, 1.0, 1.0, 1.5]
        self.gap_positions = [[1.5, 0.0, self.platform_position[2] + self.platform_size[2] / 2], [3.5, 0.0, self.platform_position[2] + self.platform_size[2] / 2], [5.5, 0.0, self.platform_position[2] + self.platform_size[2] / 2], [8.0, 0.0, self.platform_position[2] + self.platform_size[2] / 2], [11.0, 0.0, self.platform_position[2] + self.platform_size[2] / 2], [15.0, 0.0, self.platform_position[2] + self.platform_size[2] / 2]]
        self.gap_ids = []
        for i, gap_width in enumerate(self.gap_widths):
            gap_id = self.create_box(mass=0.0, half_extents=[gap_width / 2, self.platform_size[1] / 2, self.platform_size[2] / 2], position=self.gap_positions[i], color=[0.0, 0.0, 0.0, 1.0])
            self.gap_ids.append(gap_id)
        self.robot_position_init = [self.platform_position[0] - self.platform_size[0] / 2 + 0.5, self.platform_position[1], self.platform_position[2] + self.platform_size[2] / 2 + self.robot.links['base'].position_init[2]]

    def create_box(self, mass, half_extents, position, color):
        collision_shape_id = self._p.createCollisionShape(shapeType=self._p.GEOM_BOX, halfExtents=half_extents)
        visual_shape_id = self._p.createVisualShape(shapeType=self._p.GEOM_BOX, halfExtents=half_extents, rgbaColor=color)
        return self._p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_shape_id, baseVisualShapeIndex=visual_shape_id, basePosition=position)

    def reset(self):
        observation = super().reset()
        self.time = 0.0
        self._p.resetBasePositionAndOrientation(self.robot.robot_id, self.robot_position_init, self.robot.links['base'].orientation_init)
        return observation

    def step(self, action):
        self.position = self.robot.links['base'].position
        observation, reward, terminated, truncated, info = super().step(action)
        self.time += self.dt
        return (observation, reward, terminated, truncated, info)

    def get_task_rewards(self, action):
        new_position = self.robot.links['base'].position
        survival = 1.0
        gap_reward = 0.0
        for i, gap_position in enumerate(self.gap_positions):
            if self.position[0] < gap_position[0] and new_position[0] >= gap_position[0]:
                gap_reward += 1.0
        end_reward = 10.0 if new_position[0] > self.platform_size[0] / 2 else 0.0
        return {'survival': survival, 'gap_reward': gap_reward, 'end_reward': end_reward}

    def get_terminated(self, action):
        if self.robot.links['base'].position[2] < self.platform_position[2]:
            return True
        if self.robot.links['base'].position[0] > self.platform_size[0] / 2:
            return True
        return False

    def get_success(self):
        return self.robot.links['base'].position[0] > self.platform_size[0] / 2