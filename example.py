import Orange
import numpy as np
from orangecontrib.wbd import api_wrapper

api = api_wrapper.IndicatorAPI()

test_data = api.get_dataset([
    "SH.H2O.SAFE.ZS",  # Improved water source (% of population with access)
    "SH.MED.BEDS.ZS",  # Hospital beds (per 1,000 people)
    "SH.IMM.IDPT",     # Immunization, DPT (% of children ages 12-23 months)
]).as_orange_table()

class_data = api.get_dataset(
    "SP.DYN.IMRT.IN",  # Mortality rate, infant (per 1,000 live births)
).as_orange_table()

# lines with valid class values (not nan)
good_lines = ~np.isnan(np.array(class_data[:,55]))[:,0]

domain = Orange.data.Domain(
    test_data.domain.attributes, class_vars=class_data.domain[55])

data = Orange.data.Table(
    domain,
    np.array(test_data)[good_lines,:],
    np.array(class_data)[good_lines,55]
)

rf = Orange.regression.random_forest.RandomForestRegressionLearner()
ridge = Orange.regression.RidgeRegressionLearner()
mean = Orange.regression.MeanLearner()

learners = [rf, ridge, mean]

res = Orange.evaluation.CrossValidation(data, learners, k=10)
rmse = Orange.evaluation.RMSE(res)
r2 = Orange.evaluation.R2(res)

print("{:25} {:7} {:7}".format("Learner", "RMSE", "R2"))
for i in range(len(learners)):
    print("{:25} {:5.2f} {:6.2f}".format(learners[i].name, rmse[i], r2[i]))
