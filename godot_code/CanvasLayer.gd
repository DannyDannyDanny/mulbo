extends CanvasLayer

func _ready():
	$HTTPRequest.connect("request_completed", self, "_on_request_completed")

func _on_request_completed(result, response_code, headers, body):
	var json = JSON.parse(body.get_string_from_utf8())
	print(json.result)

func _on_SendButton_pressed():
	print("Sent " + $TextInput.text)
	send($TextInput.text)


func _on_OtherButton_pressed():
	print("Sent " + $TextInput.text)
	send($TextInput.text)

	
#func _process(delta):
#	pass

func send(text):
	$Output.text = text
	$HTTPRequest.request("http://www.mocky.io/v2/5185415ba171ea3a00704eed")
