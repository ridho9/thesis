from timun.runner import run_scenario
from timun.step import StepDict
from typing import List
import random

from timun.model import Feature, Scenario, ScenarioType, Step


def extract_step_from_features(features: List[Feature]) -> List[Step]:
    res: List[Step] = []
    for f in features:
        for s in f.scenarios:
            res += s.steps
    return res


class RandomScrambleStrategy:
    def __init__(self, min=3, max=6):
        self.min = min
        self.max = max

    def gen(self, steps: List[Step]) -> Scenario:
        gen_len = random.randint(self.min, min(self.max, len(steps)))
        res = random.sample(steps, gen_len)

        return Scenario(ScenarioType.FAIL_SCENARIO, "random gen", res, 0, None, None)


class Scrambler:
    def __init__(
        self,
        features: List[Feature],
        step_dict: StepDict,
        environment,
        seed=None,
        strategy=RandomScrambleStrategy(),
        amount=10,
    ):
        self.steps = extract_step_from_features(features)

        # TODO: deduplicate steps

        self.step_dict = step_dict
        self.seed = seed
        random.seed(self.seed)

        self.strategy = strategy
        self.amount = amount
        self.environment = environment

    def gen_scenario(self) -> Scenario:
        return self.strategy.gen(self.steps)

    def run(self):
        print(f"Running scrambler")
        print(f"Steps available\t\t: {len(self.steps)}")
        print(f"Seed\t\t\t: {self.seed}")
        print(f"Strategy\t\t: {self.strategy}")
        print(f"Amount to generate\t: {self.amount}")

        scenarios: List[Scenario] = []
        for _ in range(self.amount):
            scenarios.append(self.gen_scenario())

        print("==== Failed Scenarios ====")

        for scenario in scenarios:
            report = run_scenario(self.step_dict, None, scenario, self.environment)
            if report.exception:
                print(report.desc_line())
                for step in scenario.steps:
                    print("\t", step.pretty())
