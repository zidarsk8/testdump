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

class_values = np.array(class_data[:,55])
class_var = class_data.domain[55]
class_var.name = "Urban population {}".format(class_var.name)

domain = Orange.data.Domain(test_data.domain.attributes, class_vars=class_var)

good_lines = ~np.isnan(class_values[:,0])
test_data = np.array(test_data)[good_lines,:]
class_data = np.array(class_values)[good_lines,:]


data = Orange.data.Table(domain, test_data, class_data)

lin = Orange.regression.linear.LinearRegressionLearner()

res = Orange.evaluation.CrossValidation(data, [lin], k=5)

rmse = Orange.evaluation.RMSE(res)
r2 = Orange.evaluation.R2(res)

print("{:8} {:.2f} {:5.2f}".format(lin.name, rmse[0], r2[0]))



# ID: EN.ATM.NOXE.AG.ZS
# Name: Agricultural nitrous oxide emissions (% of total)  1970 - 2008
# ID: EG.ELC.RNEW.ZS
# Name: Renewable electricity output (% of total electricity output) 1990 - 2012
# ID: EG.ELC.ACCS.ZS
# Name: Access to electricity (% of population)  / 1990 2000 2010 2012
# ID: SP.URB.TOTL.IN.ZS
# Name: Urban population (% of total)  / 1960 - 2015
