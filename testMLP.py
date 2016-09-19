# -*- coding: UTF-8 -*-
__author__ = 'xuxiaoye'

import os, django

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from xiaoye.models import *
from xiaoye.common import *
import math


def dtanh(x):
    return 1.0 - x * x


class MLP:
    def setInputHiddenMappingWeightFor(self, model_inputValue, model_hiddenNode, weight):
        ihm = InputHiddenMapping.objects.filter(inputValue=model_inputValue, hiddenNode=model_hiddenNode)
        if ihm:
            ihm = ihm[0]
            ihm.weight = weight
            ihm.save()
        else:
            # New record
            ihm = InputHiddenMapping()
            ihm.inputValue = model_inputValue
            ihm.hiddenNode = model_hiddenNode
            ihm.weight = weight
            ihm.save()

    def getInputHiddenMappingWeightFor(self, model_inputValue, model_hiddenNode):
        ihm = InputHiddenMapping.objects.filter(inputValue=model_inputValue, hiddenNode=model_hiddenNode)
        if ihm:
            return ihm[0].weight
        else:
            # If no relationship, setup default value 1
            defaultWeight = -0.2
            # setInputHiddenMappingFor(model_inputValue, model_hiddenNode, defaultWeight)
            return defaultWeight

    def setHiddenOutputMappingWeightFor(self, model_hiddenNode, model_outputValue, weight):
        him = HiddenOutputMapping.objects.filter(hiddenNode=model_hiddenNode, outputValue=model_outputValue)
        if him:
            him = him[0]
            him.weight = weight
            him.save()
        else:
            # New record
            him = HiddenOutputMapping()
            him.hiddenNode = model_hiddenNode
            him.outputValue = model_outputValue
            him.weight = weight
            him.save()

    def getHiddenOutputMappingWeightFor(self, model_hiddenNode, model_outputValue):
        him = HiddenOutputMapping.objects.filter(hiddenNode=model_hiddenNode, outputValue=model_outputValue)
        if him:
            return him[0].weight
        else:
            # If no relationship, setup default value 0
            defaultWeight = 0
            # setHiddenOutputMappingFor(model_hiddenNode, model_outputValue, defaultWeight)
            return defaultWeight

    def generateHiddenNodeFor(self, model_inputValue_array, model_outputValue_array):
        # if len(model_inputValue_array) > 3:
        #     return None
        hiddenKey = '_'.join(sorted([model_inputValue.value for model_inputValue in model_inputValue_array]))
        hn = HiddenNode.objects.filter(hiddenKey=hiddenKey)
        if not hn:
            hn = HiddenNode()
            hn.hiddenKey = hiddenKey
            hn.save()
            for model_inputValue in model_inputValue_array:
                self.setInputHiddenMappingWeightFor(model_inputValue, hn, 1.0 / len(model_inputValue_array))
            for model_outputValue in model_outputValue_array:
                self.setHiddenOutputMappingWeightFor(hn, model_outputValue, 0.1)

    def getAllHiddenNodeFor(self, model_inputValue_array, model_outputValue_array):
        model_hiddenNode_dict = {}
        for ihm in InputHiddenMapping.objects.filter(inputValue__in=model_inputValue_array):
            model_hiddenNode_dict[ihm.hiddenNode_id] = 1
        for him in HiddenOutputMapping.objects.filter(outputValue__in=model_outputValue_array):
            model_hiddenNode_dict[him.hiddenNode_id] = 1
        keys = model_hiddenNode_dict.keys()
        model_hiddenNode_array = [HiddenNode.objects.get(pk=id) for id in model_hiddenNode_dict.keys()]
        return model_hiddenNode_array

    def setupNetwork(self, model_inputValue_array, model_outputValue_array):
        self.model_inputValue_array = model_inputValue_array
        self.model_hiddenNode_array = self.getAllHiddenNodeFor(model_inputValue_array, model_outputValue_array)
        self.model_outputValue_array = model_outputValue_array

        self.inputNodeOutputValue = [1.0] * len(self.model_inputValue_array)
        self.hiddenNodeOutputValue = [1.0] * len(self.model_hiddenNode_array)
        self.outputNodeOutputValue = [1.0] * len(self.model_outputValue_array)

        # Matrix Input To Hidden
        self.weightInputToHidden = [
            [self.getInputHiddenMappingWeightFor(model_inputValue, model_hiddenNode) for model_hiddenNode in
             self.model_hiddenNode_array] for model_inputValue in self.model_inputValue_array
            ]

        # Matrix Hidden To Output
        self.weightHiddenToOutput = [
            [self.getHiddenOutputMappingWeightFor(model_hiddenNode, model_outputValue) for model_outputValue in
             self.model_outputValue_array] for model_hiddenNode in self.model_hiddenNode_array
            ]
        print 'input Matirx:', self.inputNodeOutputValue
        print 'hidden Matrix', self.hiddenNodeOutputValue
        print 'output Matrix', self.outputNodeOutputValue
        print 'ItoH Weight Matrix:', self.weightInputToHidden
        print 'HtoO Weight Matrix:', self.weightHiddenToOutput

    def feedForward(self):
        for i in range(len(self.model_inputValue_array)):
            self.inputNodeOutputValue[i] = 1.0

        for j in range(len(self.model_hiddenNode_array)):
            sum = 0.0
            for i in range(len(self.model_inputValue_array)):
                sum = sum + self.inputNodeOutputValue[i] * self.weightInputToHidden[i][j]
            self.hiddenNodeOutputValue[j] = math.tanh(sum)

        for k in range(len(self.model_outputValue_array)):
            sum = 0.0
            for j in range(len(self.model_hiddenNode_array)):
                sum = sum + self.hiddenNodeOutputValue[j] * self.weightHiddenToOutput[j][k]
            self.outputNodeOutputValue[k] = math.tanh(sum)

        result = self.outputNodeOutputValue[:]
        print 'feed forward result:', result
        return result

    def getResult(self, inputs, outputs):
        self.setupNetwork(inputs, outputs)
        return self.feedForward()

    def backPropagate(self, targets, N=0.5):
        output_deltas = [0.0] * len(self.model_outputValue_array)
        for k in range(len(self.model_outputValue_array)):
            error = targets[k] - self.outputNodeOutputValue[k]
            output_deltas[k] = dtanh(self.outputNodeOutputValue[k]) * error

        print "output deltas", output_deltas
        hidden_deltas = [0.0] * len(self.model_hiddenNode_array)

        for j in range(len(self.model_hiddenNode_array)):
            error = 0.0
            for k in range(len(self.model_outputValue_array)):
                error = error + output_deltas[k] * self.weightHiddenToOutput[j][k]
            hidden_deltas[j] = dtanh(self.hiddenNodeOutputValue[j]) * error

            for j in range(len(self.model_hiddenNode_array)):
                for k in range(len(self.model_outputValue_array)):
                    change = output_deltas[k] * self.hiddenNodeOutputValue[j]
                    self.weightHiddenToOutput[j][k] = self.weightHiddenToOutput[j][k] + 0.5 * change

            for i in range(len(self.model_inputValue_array)):
                for j in range(len(self.model_hiddenNode_array)):
                    change = hidden_deltas[j] * self.inputNodeOutputValue[i]
                    self.weightInputToHidden[i][j] = self.weightInputToHidden[i][j] + 0.5 * change

        print "hidden deltas", hidden_deltas

    def trainQuery(self, model_inputValue_array, model_outputValue_array, model_outputValue):
        self.generateHiddenNodeFor(model_inputValue_array, model_outputValue_array)
        self.setupNetwork(model_inputValue_array, model_outputValue_array)
        self.feedForward()
        targets = [0.0] * len(model_outputValue_array)
        targets[model_outputValue_array.index(model_outputValue)] = 1.0
        self.backPropagate(targets)
        self.updateDatabase()

    def updateDatabase(self):
        for i in range(len(self.model_inputValue_array)):
            for j in range(len(self.model_hiddenNode_array)):
                self.setInputHiddenMappingWeightFor(self.model_inputValue_array[i], self.model_hiddenNode_array[j],
                                                    self.weightInputToHidden[i][j])
        for j in range(len(self.model_hiddenNode_array)):
            for k in range(len(self.model_outputValue_array)):
                self.setHiddenOutputMappingWeightFor(self.model_hiddenNode_array[j], self.model_outputValue_array[k],
                                                     self.weightHiddenToOutput[j][k])

    def clear(self):
        HiddenOutputMapping.objects.all().delete()
        InputHiddenMapping.objects.all().delete()
        InputValue.objects.all().delete()
        HiddenNode.objects.all().delete()
        OutputValue.objects.all().delete()

    def trainWith(self, inputStrList, outputStrList, outputStr):
        # setup initial nodes
        inputs = []
        outputs = []
        for a in inputStrList:
            input, created = InputValue.objects.get_or_create(value=a)
            if created:
                input.value = a
                input.save()
            inputs.append(input)

        for a in outputStrList:
            output, created = OutputValue.objects.get_or_create(value=a)
            if created:
                output.value = a
                output.save()
            outputs.append(output)

        # inputs = [InputValue.objects.get(value=a)
        #           for a in inputStrList]
        # outputs = [OutputValue.objects.get(value=a)
        #            for a in outputStrList]

        output = [o for o in outputs if o.value == outputStr][0]
        # print inputs
        # print outputs
        print 'before'
        # self.showResult(inputs, outputs)
        self.getResult(inputs, outputs)
        self.trainQuery(inputs, outputs, output)
        print 'after'
        self.getResult(inputs, outputs)
        # self.showResult(inputs, outputs)

    def showResult(self, inputStrList, outputStrList):
        inputs = [InputValue.objects.get(value=a)
                  for a in inputStrList]
        outputs = [OutputValue.objects.get(value=a)
                   for a in outputStrList]
        print 'show result'
        self.getResult(inputs, outputs)

    def getModelOfInputStr(self, inputStrList):
        return [InputValue.objects.get(value=m) for m in inputStrList]

    def getModelOfOutputStr(self, outputStrList):
        return [OutputValue.objects.get(value=m) for m in outputStrList]


def demo1():
    mlp = MLP()
    clear = True
    if clear:
        mlp.clear()
        inputStr = [u'热', u'冷', u'饱', u'饿']
        # inputStr = [u'热', u'冷']
        inputModelList = []
        for v in inputStr:
            i = InputValue()
            i.value = v
            i.save()
            inputModelList.append(i)
        outputStr = [u'哭', u'叫', u'笑', u'安静']
        # outputStr = [u'哭', u'笑']
        outputModelList = []
        for v in outputStr:
            o = OutputValue()
            o.value = v
            o.save()
            outputModelList.append(o)


    i = mlp.getModelOfInputStr([u'冷'])
    o = mlp.getModelOfOutputStr([u'哭', u'叫'])
    mlp.generateHiddenNodeFor(i, o)
    # i = mlp.getModelOfInputStr([u'饿'])
    # o = mlp.getModelOfOutputStr([u'哭'])
    # mlp.generateHiddenNodeFor(i, o)
    mlp.trainWith([u'冷'], [u'哭', u'叫'], u'叫')
    mlp.showResult([u'冷'], [u'叫', u'笑', u'哭', u'安静'])

    # mlp.trainWith([u'热'], [u'安静'], u'安静')
    # # mlp.trainWith([u'饱'], [u'安静', u'笑'], u'笑')
    # for i in range(10):
    #     mlp.trainWith([u'热', u'饱'], [u'安静', u'笑', u'叫'], u'笑')
    # for i in range(5):
    #     mlp.trainWith([u'冷', u'饱'], [u'安静', u'笑', u'叫'], u'安静')
    # mlp.showResult([u'饱'], [u'叫', u'笑', u'哭', u'安静'])
    # mlp.showResult([u'热'], [u'叫', u'笑', u'哭', u'安静'])
    # mlp.showResult([u'热', u'冷'], [u'叫', u'笑', u'哭', u'安静'])
    # mlp.showResult([u'热', u'冷',u'饿'], [u'叫', u'笑', u'哭', u'安静'])


def demo2():
    mlp = MLP()
    mlp.clear()
    inputStr = []
    outputStr = []
    for i in range(-5, 5):
        inputStr.append('T%d' % i)

    for v in inputStr:
        i = InputValue()
        i.value = v
        i.save()

    for i in range(-5, 5):
        outputStr.append('T%d' % i)

    for v in outputStr:
        i = OutputValue()
        i.value = v
        i.save()

    for i in range(len(inputStr)):
        newTemp = random.randint(-5, 4)
        mlp.trainWith([inputStr[i]], ['T%d' % newTemp], 'T%d' % newTemp)


demo1()
