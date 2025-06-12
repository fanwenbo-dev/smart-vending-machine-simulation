import TFunctions as TF
import numpy as np
import csv
import os

#online
def test_online_extract_decoded_data_valid():
    input = [type('MockDecodedObject', (object,), {'data': b'example'})()]
    result = TF.online_extract_decoded_data(input)
    assert result == 'example'

def test_online_extract_decoded_data_empty():
    input=[]
    result = TF.online_extract_decoded_data(input)
    assert result == None

def test_online_extract_decoded_data_invalid():
    input = [type('MockDecodedObject', (object,), {'data': b'\x80\x81'})()]
    result = TF.online_extract_decoded_data(input)
    assert result == None

def test_online_get_qrstring_drink_valid():
    input = '2a0201'
    result = TF.online_get_qrstring_drinkno(input)
    assert result == 1

def test_online_get_qrstring_drink_invalid():
    input = "123456"
    result = TF.online_get_qrstring_drinkno(input)
    assert result == 0

def test_online_decode_qr_list():
    #Check that decoded_objects is a list
    input = np.zeros((500, 500, 3), dtype=np.uint8)
    frame, result = TF.online_decode_qr(input)
    assert isinstance(result, list)

def test_online_decode_qr_modified():
    #Check that the frame has been modified (simple check)
    input = np.zeros((500, 500, 3), dtype=np.uint8)
    frame, result = TF.online_decode_qr(input)
    assert not np.array_equal(input, result)

def test_online_finddrinkinfo_name():
    assert TF.online_finddrinkinfo("name", "08") == "Sprite"
    assert TF.online_finddrinkinfo("price", "08") == "$1.30"
    assert TF.online_finddrinkinfo("name", "01") == "Orange Fanta"
    assert TF.online_finddrinkinfo("price", "01") == "$1.50"
    assert TF.online_finddrinkinfo("name", "03") == "Ice Lemon Tea"
    assert TF.online_finddrinkinfo("price", "03") == "$1.10"

#onsite
def test_onsite_join_string():
    input=[1, 5]
    test='15'
    result=TF.onsite_join_string(input)
    assert result == test

def test_onsite_format_user_input():
    input="8"
    test="08"
    result=TF.onsite_format_user_input(input)
    assert result == test






