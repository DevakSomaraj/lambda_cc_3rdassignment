import json

def lambda_handler(event, context):
    # Check if the request is from Lex or API Gateway
    is_lex_request = "sessionState" in event
    
    if is_lex_request:
        # Extract the query from Lex slots
        slots = event.get("sessionState", {}).get("intent", {}).get("slots", {})
        query = slots.get("Keywords", {}).get("value", {}).get("interpretedValue", None)
        
        if not query:
            # Return a response for missing query
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": event["sessionState"]["intent"]["name"],
                        "state": "Failed"
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Sorry, I couldn't find anything. Please try again with different keywords."
                    }
                ]
            }
        
        # Return a success response for Lex
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": event["sessionState"]["intent"]["name"],
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"I found photos matching your query '{query}': [sample1.jpg, sample2.jpg]"
                }
            ]
        }
    
    else:
        # Handle API Gateway requests
        query = event.get('queryStringParameters', {}).get('q', None)
        custom_labels = event.get('headers', {}).get('x-amz-meta-customlabels', 'No labels provided')
        
        if not query:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Query parameter "q" is required'
                })
            }
        
        # Return a sample response for API Gateway
        search_results = {
            'message': f'Search results for query "{query}"',
            'labels': custom_labels,
            'query': query
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(search_results),
            'headers': {
                'Content-Type': 'application/json'
            }
        }