import json
import logging
import re

log = logging.getLogger(__name__)

class ReadValidateRuleTriggerJson:
    """The Class is for reading the RuleTrigger Json"""
    #Reads the rules trigger json and enrich events
    def __init__(self, rules_file_path='rule_trigger.json', events_file_path='enrich_events_new.json', output_file_path='output.json'):
        self._rules_file_path = rules_file_path
        self._events_file_path = events_file_path
        self._json_rules_file = self.read_file(self._rules_file_path)
        self._json_events_file = self.read_file(self._events_file_path)
        self._result = []
        self._output_file_path = output_file_path

    #To read json file into python dict or list
    def read_file(self, path):
        """This method takes only one argument as path
        and returns the JSON data"""
        with open(path, 'r', encoding='utf-8') as f:
            json_object = json.load(f)
        return json_object

    #to write python dict to a json output file
    def write_file(self, output):
        output_json_object = json.dumps(output, indent=4)
        with open(self._output_file_path, "w") as outfile:
            outfile.write(output_json_object)

    #it will read enrich events data and apply rule trigger conditions on each event
    def applyruleoneventfile(self):
        for rule in self._json_rules_file:
            rule_satisfied= False
            rule_result = {}
            rule_result['rule_trigger_name'] = rule['rule_trigger_name']
            rule_result['events'] = []
            rule_result['alarms'] = []
            rule_result['performance_alerts'] = []
            for event in self._json_events_file:
                #apply rule on each event
                if self.applyrule(rule, event):
                    rule_satisfied = True
                    rule_result['events'].append(event)
            if rule_satisfied:
                self._result.append(rule_result)
        self.write_file(self._result)

    #apply rule conditions on events and evalute against relationship type
    def applyrule(self, rule, event):
            #expr = ""
            #base condition for evaluating the exp which includes relationship type
            previous_condition_satisfied = False
            previous_relationship_type = "or"
            for condition in rule['trigger_condition']:
                condition_satisfied, relationship_type = self.applyconditiononevent(condition, event)
                expr = f"{previous_condition_satisfied} {previous_relationship_type} {condition_satisfied} "
                previous_relationship_type = relationship_type.lower()
                previous_condition_satisfied = eval(expr)
            return previous_condition_satisfied


    #checks rule trigger condition against events and returns the result (true or false) and relationship type (and,or)
    def applyconditiononevent(self, condition, event):
        for key, value in event.items():
            if (type(value) is str or type(value) is int):
                if key == condition['column_name']:
                    #it will validate coloumn name and its value based on operator
                    condition_satisfied = self.validate(condition['operator'], condition['value'], key, value)
                    return condition_satisfied, condition['relationship_type']
            elif type(value) is dict:
                return self.applyconditiononevent(condition, value)
        return False, condition['relationship_type']

    #validate the evnt values against the rule trigger condition values
    def validate(self, condition_operator, condition_value, key, value):
        validated = False
        if condition_operator == '=':
            if value == condition_value:
                validated = True
        elif condition_operator == '!=':
            if value !=  condition_value:
                valildated = True
        elif condition_operator == ">":
            if value > condition_value:
                validated = True
        elif condition_operator == ">=":
            if value >= condition_value:
                validated = True
        elif condition_operator == "<":
            if value < condition_value:
                validated = True
        elif condition_operator == "<=":
            if value <= condition_value:
                validated = True
        elif condition_operator == "REGEX":
            try:
                if re.search(condition_value, value):
                    validated = True
            except:
                print("value is not a string:")

        return validated

validator = ReadValidateRuleTriggerJson()
validator.applyruleoneventfile()

