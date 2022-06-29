from heart.run import run_model
import pickle

def load_model():
    try: 
        with open('../rest_api_proj/heart/data/model/model.pkl', 'rb') as file:
            model = pickle.load(file)
            return model
    except FileNotFoundError: 
        run_model()

def data_transform(data_dict):
    sex_dict = {"F":0, "M":1}
    ExerciseAngina_dict = {"N":0, "Y":1}

    ST_Slope_dict = {'Down': 0.7777777777777778,
                          'Flat': 0.8282608695652174,
                          'Up': 0.19746835443037974}
    ChestPainType_dict = {'ASY': 0.7903225806451613,
                       'ATA': 0.13872832369942195,
                       'NAP': 0.35467980295566504,
                       'TA': 0.43478260869565216}
    RestingECG_dict = {'LVH': 0.5638297872340425,
                     'Normal': 0.5163043478260869,
                     'ST': 0.6573033707865169}
    
    data_dict['sex'] = sex_dict[data_dict['sex']]
    data_dict['exerciseAngina'] = ExerciseAngina_dict[data_dict['exerciseAngina']]
    data_dict['chestPainType'] = ChestPainType_dict[data_dict['chestPainType']]
    data_dict['restingECG'] = RestingECG_dict[data_dict['restingECG']]
    data_dict['ST_Slope'] = ST_Slope_dict[data_dict['ST_Slope']]

    return data_dict