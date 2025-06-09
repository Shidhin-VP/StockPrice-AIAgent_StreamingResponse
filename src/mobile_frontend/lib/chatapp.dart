import 'package:dash_chat_2/dash_chat_2.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatApp extends StatefulWidget {
  const ChatApp({super.key});

  @override
  State<ChatApp> createState() => _ChatAppState();
}

class _ChatAppState extends State<ChatApp> {
  final ChatUser _bot = ChatUser(
    id: '1',
    firstName: "AI",
    lastName: "Assistant",
  );
  final ChatUser _currentUser = ChatUser(id: '2', firstName: "Shidhin");
  final List<ChatMessage> _messages = <ChatMessage>[];
  final TextEditingController _urlController = TextEditingController();
  String url = "";

  final warningMessageofURL = SnackBar(
    content: Text("Please attach the URL"),
    duration: Duration(seconds: 1),
  );

  ChatMessage? streamingMessage;

  Future<void> getChatResponse(ChatMessage m) async {
    setState(() {
      _messages.insert(0, m);
    });

    final client = http.Client();
    final request = http.Request('POST', Uri.parse(url));
    request.headers['Content-Type'] = 'application/json';
    request.body = jsonEncode({
      'Stockquestion': m.text,
      'name': _currentUser.firstName,
    });

    try {
      final streamedResponse = await client.send(request);

      if (streamedResponse.statusCode == 200) {
        String buffer = '';
        final botMsg = ChatMessage(
          user: _bot,
          createdAt: DateTime.now(),
          text: "",
        );
        setState(() {
          _messages.insert(0, botMsg);
          streamingMessage = botMsg;
        });

        streamedResponse.stream.transform(utf8.decoder).listen(
          (chunk) {
            buffer += chunk;

            setState(() {
              _messages.remove(streamingMessage); 
              streamingMessage = ChatMessage(
                user: _bot,
                createdAt: DateTime.now(),
                text: buffer,
              );
              _messages.insert(0, streamingMessage!);
            });
          },
          onDone: () {
            client.close();
          },
          onError: (error) {
            print("Streaming error: $error");
          },
          cancelOnError: true,
        );
      } else {
        print("Failed with status: ${streamedResponse.statusCode}");
        client.close();
      }
    } catch (e) {
      print("Exception while streaming: $e");
      client.close();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blueAccent,
      appBar: AppBar(
        title: Text("Tech 42"),
        centerTitle: true,
        surfaceTintColor: Colors.amberAccent,
        elevation: 5,
      ),
      floatingActionButton: FloatingActionButton.small(
        onPressed: () {
          showDialog(
            barrierDismissible: false,
            context: context,
            builder: (context) {
              return AlertDialog(
                title: Text("Enter Your URL"),
                content: TextField(controller: _urlController),
                actions: [
                  TextButton(
                    onPressed: () {
                      url = _urlController.text;
                      _urlController.clear();
                      Navigator.of(context).pop();
                    },
                    child: Text("Attach"),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.pop(context);
                    },
                    child: Text("Decline"),
                  ),
                ],
              );
            },
          );
        },
        child: Icon(Icons.link),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.endTop,
      body: DashChat(
        currentUser: _currentUser,
        onSend: (ChatMessage m) {
          if (url.isNotEmpty) {
            getChatResponse(m);
          } else {
            ScaffoldMessenger.of(context).showSnackBar(warningMessageofURL);
          }
        },
        messages: _messages,
        inputOptions: InputOptions(
          textInputAction: TextInputAction.send,
          sendOnEnter: true,
        ),
      ),
    );
  }
}
