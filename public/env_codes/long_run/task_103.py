import os
import numpy as np
from oped.envs.r2d2.base import R2D2Env

class Env(R2D2Env):
    """
    Conveyor Belt Item Delivery

    Description:
    - The environment consists of two 5 m x 5 m platforms connected by a 5 m long conveyor belt. The conveyor belt moves from left to right at a speed of 0.5 m/s.
    - On the right platform, there are three target areas marked by 1 m x 1 m colored squares (red, green, blue). 
    - Also on the right platform, there is a dispenser that releases items onto the conveyor belt at random intervals between 2-5 seconds. The items are 0.5 m cubes colored either red, green, or blue.
    - The robot begins on the left platform. 

    Task:
    The robot must jump onto the conveyor belt, pick up the colored items, ride the conveyor to the right platform, and deliver each item to the target area matching its color. The robot should try to deliver as many items as possible to the correct targets within the time limit.

    After delivering an item, the robot must jump back onto the conveyor belt and return to the left platform before the next item is released. The robot should wait on the left platform for the next item.

    Rewards:
    - Provide a small reward for picking up an item from the conveyor belt.
    - Provide a large reward for delivering an item to the correct target area based on color.
    - Provide a small penalty for delivering an item to the wrong target area.
    - Provide a moderate penalty if the robot falls off the conveyor belt or platforms.

    Success Conditions:
    The task is considered complete if the robot successfully delivers at least 5 items to their correct target areas within the time limit.

    Time Limit:
    The robot has 3 minutes to deliver as many items as possible.

    Termination:
    The episode ends if the robot falls off the platforms or conveyor belt, or if the time limit is reached.
    """

    def __init__(self):
        super().__init__()
        self.platform_size = [5.0, 5.0, 0.5]
        self.conveyor_size = [5.0, 1.0, 0.2]
        self.conveyor_speed = 0.5
        self.item_size = [0.5, 0.5, 0.5]
        self.item_colors = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        self.target_size = [1.0, 1.0, 0.01]
        self.target_positions = [[3.5, 1.5, 0.26], [3.5, 0.0, 0.26], [3.5, -1.5, 0.26]]
        self.dispenser_position = [-2.0, 0.0, 1.0]
        self.dispense_interval_range = [2.0, 5.0]
        self.left_platform_position = [-2.5, 0.0, 0.0]
        self.left_platform_id = self.create_box(0.0, [self.platform_size[0] / 2, self.platform_size[1] / 2, self.platform_size[2] / 2], self.left_platform_position, [0.8, 0.8, 0.8, 1.0])
        self.right_platform_position = [2.5, 0.0, 0.0]
        self.right_platform_id = self.create_box(0.0, [self.platform_size[0] / 2, self.platform_size[1] / 2, self.platform_size[2] / 2], self.right_platform_position, [0.8, 0.8, 0.8, 1.0])
        self.conveyor_position = [0.0, 0.0, self.platform_size[2] / 2 + self.conveyor_size[2] / 2]
        self.conveyor_id = self.create_box(0.0, [self.conveyor_size[0] / 2, self.conveyor_size[1] / 2, self.conveyor_size[2] / 2], self.conveyor_position, [0.3, 0.3, 0.3, 1.0])
        self.target_ids = []
        for position, color in zip(self.target_positions, self.item_colors):
            target_id = self.create_box(0.0, [self.target_size[0] / 2, self.target_size[1] / 2, self.target_size[2] / 2], position, color + [0.5])
            self.target_ids.append(target_id)
        self.item_ids = []
        self.robot_position_init = [self.left_platform_position[0], self.left_platform_position[1], self.platform_size[2] + self.robot.links['base'].position_init[2] + 0.1]
        self.time_limit = 3 * 60
        self.num_items_delivered = 0
        self.next_dispense_time = None

    def create_box(self, mass, half_extents, position, color):
        collision_shape_id = self._p.createCollisionShape(shapeType=self._p.GEOM_BOX, halfExtents=half_extents)
        visual_shape_id = self._p.createVisualShape(shapeType=self._p.GEOM_BOX, halfExtents=half_extents, rgbaColor=color)
        return self._p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_shape_id, baseVisualShapeIndex=visual_shape_id, basePosition=position)

    def reset(self):
        observation = super().reset()
        self.time = 0.0
        self.num_items_delivered = 0
        self.next_dispense_time = self.time + np.random.uniform(*self.dispense_interval_range)
        for item_id in self.item_ids:
            self._p.removeBody(item_id)
        self.item_ids = []
        self._p.resetBasePositionAndOrientation(self.robot.robot_id, self.robot_position_init, self.robot.links['base'].orientation_init)
        return observation

    def step(self, action):
        self.conveyor_velocity = [self.conveyor_speed, 0.0, 0.0]
        for item_id in self.item_ids:
            item_position, _ = self._p.getBasePositionAndOrientation(item_id)
            self._p.resetBaseVelocity(item_id, self.conveyor_velocity, [0.0, 0.0, 0.0])
            if item_position[0] > self.right_platform_position[0] + self.platform_size[0] / 2:
                self._p.removeBody(item_id)
                self.item_ids.remove(item_id)
        if self.time >= self.next_dispense_time:
            self.next_dispense_time += np.random.uniform(*self.dispense_interval_range)
            color_index = np.random.randint(len(self.item_colors))
            item_id = self.create_box(1.0, [self.item_size[0] / 2, self.item_size[1] / 2, self.item_size[2] / 2], self.dispenser_position, self.item_colors[color_index] + [1.0])
            self.item_ids.append(item_id)
        observation, reward, terminated, truncated, info = super().step(action)
        self.time += self.dt
        return (observation, reward, terminated, truncated, info)

    def get_task_rewards(self, action):
        pick_up_reward = 0.0
        if len(self._p.getContactPoints(bodyA=self.robot.robot_id, linkIndexA=-1)) > 0:
            for item_id in self.item_ids:
                if len(self._p.getContactPoints(bodyA=self.robot.robot_id, bodyB=item_id, linkIndexA=-1)) > 0:
                    pick_up_reward = 1.0
                    break
        delivery_reward = 0.0
        wrong_delivery_penalty = 0.0
        for i, item_id in enumerate(self.item_ids):
            item_position, _ = self._p.getBasePositionAndOrientation(item_id)
            for j, target_id in enumerate(self.target_ids):
                if len(self._p.getContactPoints(bodyA=item_id, bodyB=target_id)) > 0:
                    if i == j:
                        delivery_reward = 10.0
                        self.num_items_delivered += 1
                    else:
                        wrong_delivery_penalty = -1.0
                    self._p.removeBody(item_id)
                    self.item_ids.remove(item_id)
                    break
        fall_off_penalty = 0.0
        robot_position = self.robot.links['base'].position
        if robot_position[2] < 0.0:
            fall_off_penalty = -5.0
        return {'pick_up_reward': pick_up_reward, 'delivery_reward': delivery_reward, 'wrong_delivery_penalty': wrong_delivery_penalty, 'fall_off_penalty': fall_off_penalty}

    def get_terminated(self, action):
        robot_position = self.robot.links['base'].position
        if robot_position[2] < 0.0:
            return True
        if self.time >= self.time_limit:
            return True
        return False

    def get_success(self):
        return self.num_items_delivered >= 5