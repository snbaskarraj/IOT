import boto3

class Database:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def create_item(self, item_data):
        response = self.table.put_item(Item=item_data)
        return response
    
    def get_item(self, item_key):
        response = self.table.get_item(Key=item_key)
        item = response.get('Item')
        return item
    
    def update_item(self, item_key, update_expression, expression_values=None):
        update_expression_attr_values = None
        if expression_values:
            update_expression_attr_values = {f':val{i}': value for i, value in enumerate(expression_values)}
        
        response = self.table.update_item(
            Key=item_key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=update_expression_attr_values,
            ReturnValues='ALL_NEW'
        )
        
        updated_item = response.get('Attributes')
        return updated_item
    
    def delete_item(self, item_key):
        response = self.table.delete_item(Key=item_key)
        return response
    
    def get_all_items(self):
        scan_response = self.table.scan()
        items = scan_response.get('Items', [])
        return items
    
    @staticmethod
    def create_dynamodb_item(obj):
        dynamodb_item = {}
        
        for key, value in obj.items():
            if isinstance(value, (str, int, float)):
                dynamodb_item[key] = {'S': str(value)}
            elif isinstance(value, bool):
                dynamodb_item[key] = {'BOOL': value}
            elif isinstance(value, list):
                dynamodb_item[key] = {'L': [Database.create_dynamodb_item(item) for item in value]}
            elif isinstance(value, dict):
                dynamodb_item[key] = {'M': Database.create_dynamodb_item(value)}
            elif value is None:
                dynamodb_item[key] = {'NULL': True}
            else:
                raise ValueError(f"Unsupported data type for key '{key}'")
        
        return dynamodb_item

