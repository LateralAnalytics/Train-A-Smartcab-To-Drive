

actionDictionary = {'action_left': 4,'action_right': 4,'action_forward': 3,'action_none': 2}
actionMax = sorted(actionDictionary, key=actionDictionary.__getitem__, reverse=True)
print actionMax