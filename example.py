import Orange
import numpy as np
from orangecontrib.wbd import api_wrapper

api = api_wrapper.IndicatorAPI()

test_data = api.get_dataset([
  "EG.ELC.RNEW.ZS",  # Renewable electricity output (% of total electricity output)
  "EG.ELC.ACCS.ZS",  # Access to electricity (% of population)
]).as_orange_table()

class_data = api.get_dataset(
  "SP.URB.TOTL.IN.ZS",  # Urban population (% of total)
).as_orange_table()

domain = Orange.data.Domain(
    test_data.domain.attributes, class_vars=class_data.domain[55])

data = Orange.data.Table(
    domain, np.array(test_data), np.array(class_data[:,55]))

lin = Orange.regression.linear.LinearRegressionLearner()

res = Orange.evaluation.CrossValidation(data, [lin], k=5)

rmse = Orange.evaluation.RMSE(res)
r2 = Orange.evaluation.R2(res)

print("{:8} {:.2f} {:5.2f}".format(lin.name, rmse[0], r2[0]))
