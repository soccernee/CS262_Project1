import time
import config

def marshal(request_type, sender_id = '-1', receiver_id = '-1', message=''):
    # create a msg object of the values
    msg = {
        'request_type': request_type,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'timestamp': time.time(),
        'message': message
    }
        
    # convert the msg object into a single string, with :: as the delimiter between fields
    marshaled_str = ""
    for key in msg:
        marshaled_str += str(msg[key]) + "::"

    # return the marshaled string, encoded into ascii
    return marshaled_str.encode('ascii')

def unmarshal(bdata):
    str = bdata.decode('ascii')
    split_str = str.split("::") 

    if len(split_str) != 6:
        print("ERROR STR: ", str)
        raise Exception('Unable to unmarshal the request')

    msg = {}
    for i, item in enumerate(split_str):
        if i == 0:
            msg['request_type'] = int(item)
        if i == 1:
            msg['sender_id'] = item
        if i == 2:
            msg['receiver_id'] = item
        if i == 3:
            msg['timestamp'] = float(item)
        if i == 4:
            msg['message'] = item

    return msg


def marshal_response(response_code = 0, message=''):
    # create a msg object of the values
    msg = {
        'response_code': response_code,
        'timestamp': time.time(),
        'message': message
    }
        
    # convert the msg object into a single string, with :: as the delimiter between fields
    marshaled_str = ""
    for key in msg:
        marshaled_str += str(msg[key]) + "::"

    # return the marshaled string, encoded into ascii
    return marshaled_str.encode('ascii')

def unmarshal_response(bdata):
    str = bdata.decode('ascii')
    split_str = str.split("::") 

    if len(split_str) != 4:
        print("ERROR STR: ", str)
        raise Exception('Unable to unmarshal the response')

    msg = {}
    for i, item in enumerate(split_str):
        if i == 0:
            msg['response_code'] = int(item)
        if i == 1:
            msg['timestamp'] = float(item)
        if i == 2:
            msg['message'] = item
        
    return msg