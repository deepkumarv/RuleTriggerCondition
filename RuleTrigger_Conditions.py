import json
import logging
import re

log = logging.getLogger(__name__)


class ReadValidateRuleTriggerJson:
    """The Class is for reading the RuleTrigger Json"""

    def __init__(self, path='rule_trigger.json'):
        self._path = path
        print(path)
        self._rule_trigger_name = None
        self._trigger_priority = None
        self._topic = None
        self._column_name = None
        self._operator = None
        self._value = None
        self._relationship_type = None
        self.json_file = self.read_file()

    def read_file(self):
        """This method takes only one argument as path
        and returns the JSON data"""
        with open(self._path, 'r', encoding='utf-8') as f:
            json_object = json.load(f)
        #print('Rule Trigger JSON file READ. {}'.format(json_object))
        return json_object

    # returns the list of valid rule_trigger_name list
    def get_rule_trigger_name_list(self):
        rule_trigger_name_list = []
        # obj_json = json.loads(self.read_file())
        for obj in self.json_file:
            rule_trigger_name_list.append(obj['rule_trigger_name'])
        return rule_trigger_name_list

    # returns the list of valid trigger_priority list
    def get_trigger_priority_list(self):
        trigger_priority_list = []
        for obj in self.json_file:
            trigger_priority_list.append(obj['trigger_priority'])
        return trigger_priority_list

    # returns the list of valid topic list
    def get_topic_list(self):
        topic_list = []
        for obj in self.json_file:
            if self._rule_trigger_name and self._trigger_priority:
                if obj['rule_trigger_name'] == self._rule_trigger_name and \
                        obj['trigger_priority'] == self._trigger_priority:
                    for trigger_condition_obj in obj['trigger_condition']:
                        topic_list.append(trigger_condition_obj['topic'])
            elif self._rule_trigger_name:
                if obj['rule_trigger_name'] == self._rule_trigger_name:
                    for trigger_condition_obj in obj['trigger_condition']:
                        topic_list.append(trigger_condition_obj['topic'])
            elif self._trigger_priority:
                if obj['trigger_priority'] == self._trigger_priority:
                    for trigger_condition_obj in obj['trigger_condition']:
                        topic_list.append(trigger_condition_obj['topic'])
            else:
                for trigger_condition_obj in obj['trigger_condition']:
                    topic_list.append(trigger_condition_obj['topic'])
        return topic_list

    # returns the list of valid column_name list
    def get_column_name_list(self):
        column_name_list = []
        for obj in self.json_file:
            if self._rule_trigger_name and self._trigger_priority:
                if obj['rule_trigger_name'] == self._rule_trigger_name and obj['trigger_priority'] == self._trigger_priority:
                    for trigger_condition_obj in obj['trigger_condition']:
                        if self._topic:
                            if trigger_condition_obj['topic'] == self._topic:
                                column_name_list.append(trigger_condition_obj['column_name'])
                        else:
                            column_name_list.append(trigger_condition_obj['column_name'])
            elif self._rule_trigger_name:
                if obj['rule_trigger_name'] == self._rule_trigger_name:
                    for trigger_condition_obj in obj['trigger_condition']:
                        if self._topic:
                            if trigger_condition_obj['topic'] == self._topic:
                                column_name_list.append(trigger_condition_obj['column_name'])
                        else:
                            column_name_list.append(trigger_condition_obj['column_name'])
            elif self._trigger_priority:
                if obj['trigger_priority'] == self._trigger_priority:
                    for trigger_condition_obj in obj['trigger_condition']:
                        if self._topic:
                            if trigger_condition_obj['topic'] == self._topic:
                                column_name_list.append(trigger_condition_obj['column_name'])
                        else:
                            column_name_list.append(trigger_condition_obj['column_name'])
            else:
                for trigger_condition_obj in obj['trigger_condition']:
                    if self._topic:
                        if trigger_condition_obj['topic'] == self._topic:
                            column_name_list.append(trigger_condition_obj['column_name'])
                    else:
                        column_name_list.append(trigger_condition_obj['column_name'])
        return column_name_list

    # returns the list of valid operator list
    def get_operator_list(self, column_name, rule_trigger_name=None, trigger_priority=None, topic=None):
        operator_list = []

        for obj in self.json_file:
            '''if obj['rule_trigger_name'] == rule_trigger_name and obj['trigger_priority'] == trigger_priority:'''
            for trigger_condition_obj in obj['trigger_condition']:
                #print("COLUMN NAME CHECKING IN EACH JSON OBJECT:", column_name, trigger_condition_obj['operator'] )
                '''if trigger_condition_obj['topic'] == topic and trigger_condition_obj['column_name'] == column_name:'''
                if trigger_condition_obj['column_name'] == column_name:

                    operator_list.append(trigger_condition_obj['operator'])
        #print("OPERATOR LIST:", operator_list)
        return operator_list

    # returns the list of valid value list
    def get_value_list(self, column_name, operator, rule_trigger_name=None, trigger_priority=None, topic=None):
        value_list = []
        for obj in self.json_file:
            '''if obj['rule_trigger_name'] == rule_trigger_name and obj['trigger_priority'] == trigger_priority:'''
            for trigger_condition_obj in obj['trigger_condition']:
                '''if trigger_condition_obj['topic'] == topic and trigger_condition_obj[
                    'column_name'] == column_name and trigger_condition_obj['operator'] == operator:'''
                if trigger_condition_obj['column_name'] == column_name and trigger_condition_obj['operator'] == operator:
                    value_list.append(trigger_condition_obj['value'])
        return value_list

    # returns the list of valid relationship_type
    def get_relationship_type_list(self, rule_trigger_name, trigger_priority, topic, column_name):
        relationship_type_list = []
        for obj in self.json_file:
            if obj['rule_trigger_name'] == rule_trigger_name and obj['trigger_priority'] == trigger_priority:
                for trigger_condition_obj in obj['trigger_condition']:
                    if trigger_condition_obj['topic'] == topic and trigger_condition_obj['column_name'] == column_name:
                        relationship_type_list.append(trigger_condition_obj['relationship_type'])
        return relationship_type_list

    global_rule_trigger_name = ""
    def find_rule_trigger_name(self, column_name, operator, value):
        for obj in self.json_file:
            for trigger_condition_obj in obj['trigger_condition']:
                if trigger_condition_obj['column_name'] == column_name and trigger_condition_obj['operator'] == operator and trigger_condition_obj["value"]==value:
                    self.global_rule_trigger_name = obj["rule_trigger_name"]
                    print("self.global_rule_trigger_name", column_name, self.global_rule_trigger_name)

    global_relationship_type = ""
    def find_relationship_type(self, column_name, operator, value):
        for obj in self.json_file:
            for trigger_condition_obj in obj['trigger_condition']:
                print(column_name, operator, value)
                if trigger_condition_obj['column_name'] == column_name and trigger_condition_obj['operator'] == operator and trigger_condition_obj["value"] == value:
                    print("condition is true:")
                    print(obj)
                    self.global_relationship_type = trigger_condition_obj['relationship_type']
                    print("self.global_relationship_type", self.global_relationship_type)
                    return self.global_relationship_type


        # To validate when the enriched data in key value pairs
    def validate(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'rule_trigger_name':
                self._rule_trigger_name = value
                if value in self.get_rule_trigger_name_list():
                    return True
            elif key == 'trigger_priority':
                #self._trigger_priority = value
                if value in self.get_trigger_priority_list():
                    return True
            elif key == 'topic':
                #self._topic = value
                if value in self.get_topic_list():
                    return True
            elif key == 'column_name':
                self._column_name = value
                if value in self.get_column_name_list():
                    return True
            elif key == 'operator':
                #print("OPERATOR:", value)
                self._operator = value
                if value in self.get_operator_list(column_name=self._column_name):
                    return True
            elif key == 'value':
                self._value = value
                #print("SELF VALUE:", value)
                operator_list = self.get_operator_list(column_name=self._column_name)
                #print("OPERATOR LIST:", operator_list)
                for each_operator in operator_list:
                    #print("OPERATOR LIST-1:", operator_list,"EACH OPERATOR-1:", each_operator)
                    self._operator = each_operator
                    #print("SELF OPERATOR-1:", self._operator)
                    value_list = self.get_value_list(column_name=self._column_name, operator=self._operator)
                    #print("VALUE LIST:", value_list)
                    #print("SELF COLUMN NAME:", self._column_name)
                    #print("SELF _OPERATOR:", self._operator)
                    for each_value in value_list:
                        #print("TYPE OF VALUE:", type(value))
                        #print("EACH VALUE:", each_value)
                        #self.find_rule_trigger_name(self._column_name, self._operator, each_value)
                        self._value = each_value

                        if self._operator == "=":
                            if value == each_value:
                                self.find_rule_trigger_name(self._column_name, self._operator, each_value)
                                return True

                        # Regex
                        if self._operator == "REGEX":
                            #if value == each_value:
                            #if re.search(rf"\b(?=\w){value}\b(?!\w)", subject, re.IGNORECASE):
                            print("value:", value)
                            print("each_value:", each_value)
                            try:
                                if re.search(each_value, value):
                                    print(each_value, value)
                                    return True
                            except:
                                print("value is not string:")

                        if self._operator == "!=":
                            if value != each_value:
                                return True
                        if type(value)  == "int":
                            #print("VALUE COMPARISON:", value, each_value)
                            if self._operator == ">=":
                                if value >= each_value:
                                    return True
                            if self._operator == "<=":
                                if value <= each_value:
                                    return True
                            if self._operator == ">":
                                if value > each_value:
                                    return True
                            if self._operator == "<":
                                if value < each_value:
                                    return True
            elif key == 'relationship_type':
                self._relationship_type = value
                if value in self.get_relationship_type_list():
                    return True
            else:
                return False
        return False

    '''Apply Rule Trigger Conditions on Enrich events data'''
    def validate_enriched_data(self, path = "enrich_events_new.json"):
    #def validate_enriched_data(self, enriched_file_path):
        with open("enrich_events_new.json", 'r', encoding='utf-8') as f:
            json_object = json.load(f)
        new_obj = []
        new_raw_obj = []
        final_result_list = []
        result_obj = {}

        final_result = []

        final_result_2 = {}
        final_result_2["rule_trigger_name"] = []
        final_result_2["events"] = []

        relationship_type = "or"
        for obj in json_object:

            global_rule_trigger_name_list = []
            #print("controller_hostname:", obj['controller_hostname'])
            raw_obj = obj
            add_this_obj_to_result = False
            value_exists = False
            for key, enrich_value in list(obj.items()):
                if type(enrich_value)==str or type(enrich_value)==int:
                    value_exists = False
                    key_exists = v.validate(column_name=key)
                    if key_exists:
                        #operator_exists = v.validate(operator= "=")
                        #if operator_exists:
                            value_exists = v.validate(value=enrich_value)
                    #print('value_exists {}'.format(value_exists))
                    if value_exists:
                        expr = f"{add_this_obj_to_result} {relationship_type} {value_exists}"
                        print (expr)
                        add_this_obj_to_result = eval(expr)

                        relationship_type = self.find_relationship_type(self._column_name, self._operator, self._value).lower()

                    #print("VALUE NOT EXISTS:")
                    #else:
                    #obj.pop(key)
                elif type(enrich_value)== dict:
                    for key_2, enrich_value_2 in list(enrich_value.items()):
                        if type(enrich_value_2)==str or type(enrich_value_2)==int:
                            #value_exists_2 = False
                            key_exists_2 = v.validate(column_name=key_2)
                            if key_exists_2:
                                #operator_exists_2 = v.validate(operator= "=")
                                #if operator_exists_2:
                                    value_exists = v.validate(value=enrich_value_2)
                            if value_exists:
                                add_this_obj_to_result = True
                            #enrich_value.pop(key_2)
                            #else:
                                #print("VALUE NOT EXISTS:")

            #print('new_value {}'.format(value_exists))
#Below will return distinct rule trigger name with matched trigger conditions
                if add_this_obj_to_result:
                    global_rule_trigger_name_list.append(self.global_rule_trigger_name)
            if add_this_obj_to_result:
                for rule_name in global_rule_trigger_name_list:
                    rule_name_already_there_final_result = False
                    for rule_object in final_result:
                        if rule_object['rule_trigger_name'] == rule_name:
                            rule_name_already_there_final_result = True
                            rule_object['events'].append(obj)
                    if rule_name_already_there_final_result is False:
                        rule_object = {}
                        rule_object["rule_trigger_name"] = rule_name
                        rule_object["events"] = [obj]
                        rule_object["alarms"] = []
                        rule_object["performance_alerts"] = []
                        final_result.append(rule_object)
#To get the output in python dict format
                for rule_name_2 in global_rule_trigger_name_list:
                    final_result_2["rule_trigger_name"].append(rule_name_2)
                    final_result_2["events"].append(obj)
                    final_result_2["alarms"] = []
                    final_result_2["performance_alerts"] = []

                #obj["rule_trigger_name"] = self.global_rule_trigger_name
                #raw_obj["rule_trigger_name"] = self.global_rule_trigger_name
                #new_obj.append(obj)
                #new_raw_obj.append(raw_obj)
                #result_obj = {}
                #result_obj["rule_trigger_name"] = self.global_rule_trigger_name
                #result_obj["events"] = new_obj
                # result_obj["alarms"] = []
                # result_obj["performance_alerts"] = []
                # final_result_list.append(result_obj)
        #print('NEW OBJ {}'.format(new_obj))
        #return new_obj
        return final_result, final_result_2

v = ReadValidateRuleTriggerJson()
#print(v.validate(rule_trigger_name="Rule Trigger from JSON one"))
#print(v.validate(trigger_priority=1))
#print(v.validate(topic="Alarm Topic"))
#print(v.validate(topic="Event Topics"))
#print(v.validate(column_name="eventId"))
#print(v.validate(column_name="host_name"))
#print(v.validate(column_name="device"))
#print(v.validate(column_name="accountId"))
#print(v.validate(operator="="))
#print(v.validate(value="355"))

output, output_2 = v.validate_enriched_data("enrich_events_new.json")
output_json_object = json.dumps(output, indent=4)
with open("final_output_rt.json", "w") as outfile:
    outfile.write(output_json_object)
#print(output)
output_json_object_2 = json.dumps(output_2, indent=4)
with open("final_output_rt_2.json", "w") as outfile:
    outfile.write(output_json_object_2)


