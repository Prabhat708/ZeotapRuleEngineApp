from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserData, Rule
import json
import re
 
def index(request):
    return render(request, 'index.html')


def get_rules(request):
    if request.method == 'GET':
        rules = list(Rule.objects.all().values('id', 'rule'))  # Fetch predefined rules
        return JsonResponse({'rules': rules})

@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = UserData.objects.create(
            age=data['age'],
            salary=data['salary'],
            department=data['department'],
            experience=data['experience']
        )
        return JsonResponse({'message': 'User data added successfully'}, status=201)

@csrf_exempt
def add_rule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            custom_rule = data.get('rule')

            if not custom_rule:
                return JsonResponse({'error': 'Rule cannot be empty'}, status=400)
            if Rule.objects.filter(rule__iexact=custom_rule).exists():
                return JsonResponse({'error': 'This rule already exists'}, status=400)

            # Save the custom rule to the database
            new_rule = Rule(rule=custom_rule)
            new_rule.save()

            return JsonResponse({'message': 'Custom rule added successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
@csrf_exempt
def evaluate_user(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            # print(f"Received data: {data}")  # Debugging line

            rule_id = data.get('rule_id')  # Get selected predefined rule (if any)
            custom_rule = data.get('custom_rule')  # Get custom rule (if provided)
            user_data = data.get('user_data')  # Extract user data

            # Validate incoming user data
            if not user_data or not isinstance(user_data, dict):
                return JsonResponse({'error': 'Invalid user data'}, status=400)

            # Get the rule to evaluate
            if rule_id:
                rule = Rule.objects.get(id=rule_id).rule  # Fetch the predefined rule by ID
            elif custom_rule:
                rule = custom_rule  # Use the custom rule provided by the user
            else:
                return JsonResponse({'error': 'No rule provided'}, status=400)

            # Parse the rule into AST
            ast = create_rule(rule)
            # print(f"AST generated: {ast}")  # Debugging line

            if ast is None:
                return JsonResponse({'error': 'Invalid rule format'}, status=400)

            # Evaluate the user data based on the rule
            if evaluate_rule(ast, user_data):
                return JsonResponse({'eligible': True, 'rule': rule})
            else:
                return JsonResponse({'eligible': False, 'rule':rule})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            # print(f"Error occurred during evaluation: {str(e)}")  # used for debugging
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def create_rule(rule_string):
    # print(f"Creating rule for: {rule_string}")  # used for debugging
    condition_pattern = r"(\w+) *([><=]+|=) *(\d+|'[^']+'|\"[^\"]+\")"

    # Split the rule string while capturing parentheses
    tokens = re.split(r'(\s+AND\s+|\s+OR\s+|\(|\))', rule_string)
    tokens = [token.strip() for token in tokens if token.strip()]
    # print(f"Tokens: {tokens}")  # Debugging line

    def parse_tokens(tokens):
        """ Recursively parse tokens into an AST """
        def parse_expression():
            expression = []
            while tokens:
                token = tokens.pop(0)
                # print(f"Processing token: {token}")  # Debugging line

                if token == '(':
                    # Recursively parse sub-expressions inside parentheses
                    expression.append(parse_expression())
                elif token == ')':
                    break
                else:
                    # Add token (either condition or operator) to the current expression
                    expression.append(token)

            return expression

        return parse_expression()

    ast_tokens = parse_tokens(tokens)
    # print(f"AST Tokens: {ast_tokens}")  # Debugging line
    ast = build_ast(ast_tokens, condition_pattern)
    # print(f"AST Generated: {ast}")  # Debugging line
    return ast
def build_ast(tokens, condition_pattern):
    # Recursively build the AST from the list of tokens.
    # print(f"Building AST from tokens: {tokens}")  # Debugging line

    # Handle a single operand condition
    if isinstance(tokens, str):
        condition = re.match(condition_pattern, tokens)
        if condition:
            attribute, operator, value = condition.groups()
            # print(f"Condition matched: {attribute} {operator} {value}")  # Debugging line
            return {'type': 'operand', 'value': f"{attribute} {operator} {value}"}
        
    
    # Handle binary operators like AND, OR
    for operator in ['OR', 'AND']:
        if operator in tokens:
            operator_idx = tokens.index(operator)
            # print(f"Found operator: {operator}")  # Debugging line
            left = build_ast(tokens[:operator_idx], condition_pattern)
            right = build_ast(tokens[operator_idx + 1:], condition_pattern)
            return {'type': 'operator', 'left': left, 'right': right, 'value': operator}

    # If tokens are still a list and not just a string condition
    if isinstance(tokens, list):
        # Recursively build AST for nested expressions
        return build_ast(tokens[0], condition_pattern)

    # print(f"Returning None for tokens: {tokens}")  # Debugging line
    return None
def evaluate_rule(ast, data):
    if ast is None:
        # print("Error: AST is None!")  # used for debugging
        return False
    
    if ast['type'] == 'operand':
        # print(f"Evaluating operand: {ast['value']}") # used for debugging
        attribute, operator, value = ast['value'].split()

        # Handle numerical vs string values
        if value.isdigit():
            value = int(value)
        else:
            value = value.strip("'").strip('"')  # Handle strings with single or double quotes

        actual_value = data.get(attribute)
        if actual_value is None:
            # print(f"Warning: Attribute {attribute} not found in user data") # used for debugging
            return False

        # Perform comparison
        if operator == '>':
            return int(actual_value) > value
        elif operator == '<':
            return int(actual_value) < value
        elif operator in ['=', '==']:
            return actual_value == value  

    elif ast['type'] == 'operator':
        # print(f"Evaluating operator: {ast['value']}") # used for debugging
        left_eval = evaluate_rule(ast['left'], data) if ast['left'] else False
        right_eval = evaluate_rule(ast['right'], data) if ast['right'] else False

        if ast['value'] == 'AND':
            return left_eval and right_eval
        elif ast['value'] == 'OR':
            return left_eval or right_eval

    # print(f"Error: Unrecognized AST node type or incomplete AST: {ast}")  # Debugging line
    return False
