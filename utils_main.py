import gym
import os
from datetime import datetime
import torch
import numpy as np
import csv

# used to save the best results


def make_env(env_name):
    def _thunk():
        env = gym.make(env_name)
        return env

    return _thunk


class save_files:
    def __init__(self):
        self.date = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
        self.current_dir = os.getcwd()
        self.path_step_reward = "results/reward_step"
        self.path_diverge = f"results/diverge_data{self.date}"

        self.path_best_reward = f"results/bestreward{self.date}"
        self.path_model = f"results/model{self.date}"
        self._save_init(self.path_step_reward)
        self._save_init(self.path_best_reward)
        self._save_init(self.path_model)
        self._save_init(self.path_diverge)
        self.index = 1
        self.i_diverge = 0
        self.diverge_count = 0

        fields = ["counter", "step", "reward"]
        with open(f"{self.path_step_reward}/reward_step{self.date}.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    def _save_init(self, directory):
        self.path = os.path.join(self.current_dir, directory)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def best_reward_save(
        self,
        all_t,
        all_actions,
        all_obs,
        all_rewards,
        control_rewards,
        header,
        control_input=np.array((0.0, 0.0, 0.0, 0.0)),
    ):
        date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        if any(control_input):

            np.savetxt(
                f"{self.path_best_reward}/best_rewards{date}.csv",
                np.c_[all_t, all_actions, all_obs, all_rewards, control_input, control_rewards],
                delimiter=",",
                header=header,
            )
        else:
            np.savetxt(
                f"{self.path_best_reward}/best_rewards{date}.csv",
                np.c_[all_t, all_actions, all_obs, all_rewards, control_rewards],
                delimiter=",",
                header=header,
            )

    def reward_step_save(self, best_rew, longest_step, curr_tot_rew, curr_step):
        print(f"best reward: {best_rew}, longest step: {longest_step}, reward: {curr_tot_rew}, step: {curr_step} ")
        fields = [self.index, curr_step, float(curr_tot_rew)]
        with open(f"{self.path_step_reward}/reward_step{self.date}.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        self.index += 1

    def model_save(self, model):
        date = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
        torch.save(model.state_dict(), f"{self.path_model}/model{date}.pt")

    def diverge_save(self, obs_dict, observation_count):
        if self.i_diverge == 0:
            self.header_diverge = ""
            for elem in obs_dict.keys():
                self.header_diverge += elem + ", "
            self.i_diverge = 1
            self.a = np.zeros(len(obs_dict))
        self.a[observation_count] += 1
        self.diverge_count += 1
        if self.diverge_count == 1000:
            np.savetxt(
                f"{self.path_diverge}/diverge.csv",
                self.a.reshape(1, self.a.shape[0]),
                header=str(self.header_diverge),
                delimiter=",",
                fmt="%d",
            )
            self.diverge_count = 0
