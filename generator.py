import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #Initiate diagnosis
        diagnosis = 'No Diagnosis Met'
        
        #Does duration meet the criterium?
        mddCurrentDruation = request.form.getlist('mddCurrentDuration')
        mddDurationSatisfaction = openai.Completion.create(
                model="text-davinci-003",
                prompt=duration_prompt(mddCurrentDruation, '2 weeks'),
                temperature=0, max_tokens=100
            )
        print(mddDurationSatisfaction)
        
        durationMet = mddDurationSatisfaction.choices[0].text
        
        
        mddSymptoms = [
              "Depressive mood",
              "Anhedonia",
              "Changes in Appetite/Weight",
              "Changes in Sleep",
              "Changes in Psychomotor",
              "Fatigue",
              "Worthlessness or Guilt",
              "Concentration Difficulties/Indecisiveness",
              "Suicidality"
            ]
        
        mddCurrentSymptom = request.form.getlist('mddCurrentSymptom')
        mddCurrentSymptomExample = request.form.getlist('mddCurrentSymptomExample')
        mddCurrentSymptomExample = mddCurrentSymptomExample + [''] 
        
        mddCurrentSymptomListwExample = ['']*len(mddSymptoms)
        i = 0
        for symptom in mddSymptoms:
            if symptom in mddCurrentSymptom:
                if mddCurrentSymptomExample[i]:
                    mddCurrentSymptomListwExample[i] = symptom + ' (' + mddCurrentSymptomExample[i] + ')'
                else:
                    mddCurrentSymptomListwExample[i] = symptom 
            i+=1
               
        mddCurrentSymptomCritical = mddCurrentSymptomListwExample[0:2]
        
        mddCurrentSymptomCriticalCount = 0
        for symptom in mddCurrentSymptomCritical:
            if symptom != '':
                mddCurrentSymptomCriticalCount += 1
                
        mddCurrentSymptomAdditional = mddCurrentSymptomListwExample[2:]
        mddCurrentSymptomAdditionalCount = 0
        for symptom in mddCurrentSymptomAdditional:
            if symptom != '':
                mddCurrentSymptomAdditionalCount += 1
        
        print(mddCurrentSymptomCriticalCount, mddCurrentSymptomAdditionalCount)
        
        symptomCount = mddCurrentSymptomCriticalCount + mddCurrentSymptomAdditionalCount
        
        suicideDescription = request.form.getlist('suicideDescription')
        
        suicideLabel = ['passive death thoughts', 'active suicidal thoughts', 'plan', 'intent', 'past suicidal attempts']
        for i in range(len(suicideLabel)):
            suicideLabel[i] = suicideLabel[i] + ': ' + suicideDescription[i]
        
        #MDD HPI
        hpi_description = ''
        
        if mddCurrentSymptomCriticalCount>=1 and symptomCount >=5 and 'Yes' in durationMet:
            mddCurrentDescription = openai.Completion.create(
                model="text-davinci-003",
                prompt=mdd_symptom_prompt(mddCurrentSymptomCritical, mddCurrentSymptomAdditional, mddCurrentDruation),
                temperature=0.1, max_tokens=1000
            )
            hpi_description += mddCurrentDescription.choices[0].text
            diagnosis = 'Major Depressive Disorder'
            
            print(mddCurrentDescription)
        
        #Suicidality
        if len(set(suicideDescription))>1:
            suicidalityDescription = openai.Completion.create(
                model="text-davinci-003",
                prompt=suicidality_description_prompt(suicideLabel),
                temperature=0, max_tokens=1000
            )
            hpi_description += suicidalityDescription.choices[0].text
            print(suicidalityDescription)
        
        
        return render_template('report.html', hpi_description=hpi_description, diagnosis_description=diagnosis)
    
    return render_template('index.html')
        

def duration_prompt(currDuration, requiredDuration):
    return """
    One month eauls four weeks. One year equals 12 months. Decide whether {} is longer than {}. 
    """.format(currDuration, requiredDuration)


def mdd_symptom_prompt(symptomCritical, symptomAdditional, duration):
    return """
    Critical symptoms: {}
    Additional symptoms: {}
    Insert the list of symptoms in lowercase to the following sentneces with correct grammar and a medical tone. In the past {}, Pt expericed [critical symptoms] most of the day, almosst every day. These symptoms were accompanied by [additional symptoms].""".format(symptomCritical, symptomAdditional, duration)

def suicidality_description_prompt(suicideLabel):
    return """Describe Pt's suicidality using the following information: {}, using a medical tone.""".format(suicideLabel)


if __name__ == '__main__':
    app.run(debug=True)