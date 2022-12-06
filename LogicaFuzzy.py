import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def main():
    
    atividade_fisica = ctrl.Antecedent(np.arange(0, 8, 1), 'Atividade fisica')
    alimentacao = ctrl.Antecedent(np.arange(0, 11, 1), 'Alimentação')
    peso = ctrl.Consequent(np.arange(30, 200, 60), 'Peso')

    atividade_fisica['Otima'] = fuzz.trapmf(atividade_fisica.universe, [0, 1, 2, 4])
    atividade_fisica['Ok'] = fuzz.trapmf(atividade_fisica.universe, [2, 5, 5, 6])
    atividade_fisica['Ruim'] = fuzz.trapmf(atividade_fisica.universe, [4, 8, 8, 10])
    
    alimentacao['Otima'] = fuzz.trimf(alimentacao.universe, [0, 1, 2,])
    alimentacao['Ok'] = fuzz.trimf(alimentacao.universe, [1, 5, 6,])
    alimentacao['Ruim'] = fuzz.trimf(alimentacao.universe, [5, 8, 10])
    
    peso['Baixo-peso'] = fuzz.gaussmf(peso.universe, 40, 25)
    peso['Peso-normal'] = fuzz.gaussmf(peso.universe, 70, 25)
    peso['Sobrepeso'] = fuzz.gaussmf(peso.universe, 120, 25)
    peso['Obeso'] = fuzz.gaussmf(peso.universe, 150, 25)  

    regra_1 = ctrl.Rule(atividade_fisica['Otima'] & alimentacao['Otima'], peso['Baixo-peso'])
    regra_2 = ctrl.Rule(atividade_fisica['Ok'] | alimentacao['Ok'], peso['Peso-normal'])
    regra_3 = ctrl.Rule(atividade_fisica['Ruim'] | alimentacao['Ok'], peso['Sobrepeso'])
    regra_4 = ctrl.Rule(alimentacao['Ruim'] & atividade_fisica['Ruim'], peso['Obeso'])

    controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3,regra_4])

    Calculopeso = ctrl.ControlSystemSimulation(controlador)
    notaAtividade = int(input('Atividade fisica: '))
    notaServico = int(input('Alimentação: '))
    Calculopeso.input['Atividade fisica'] = notaAtividade
    Calculopeso.input['Alimentação'] = notaServico
    Calculopeso.compute()

    valorpeso = Calculopeso.output['Peso']

    print("\nAtividade fisica %d \nAlimentacao %d \nPeso de %5.2f" %(
            notaAtividade,
            notaServico,
            valorpeso))

    atividade_fisica.view(sim = Calculopeso)
    alimentacao.view(sim = Calculopeso)
    peso.view(sim = Calculopeso)

    plt.show()
main() 
