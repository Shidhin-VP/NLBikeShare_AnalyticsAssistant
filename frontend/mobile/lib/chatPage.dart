import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:dash_chat_2/dash_chat_2.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final ChatUser user = ChatUser(id: '1', firstName: '~');

  List<ChatMessage> messages = [];

  Future<String> sendQuestiontoBackend(String question) async {
    final endpoint = dotenv.env['endPoint'];
    final response = await http.post(
      Uri.parse(endpoint!),
      headers: {"Content-Type": 'application/json'},
      body: jsonEncode({"question": question}),
    );
    if (response.statusCode == 200) {
      return response.body;
    } else {
      throw Exception("Failed With Status ${response.statusCode}");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("ChatPage"),
        centerTitle: true,
        elevation: 5,
        backgroundColor: Colors.deepOrangeAccent,
      ),
      body: SafeArea(
        child: DashChat(
          currentUser: user,
          onSend: (ChatMessage message) async {
            setState(() {
              messages.insert(0, message);
            });
            try {
              String reply = await sendQuestiontoBackend(message.text);
              print("Reply: $reply");
              // final Map<String, dynamic> decoded = jsonDecode(reply);
              final botMessage = ChatMessage(
                user: ChatUser(id: '2', firstName: "Assistant"),
                text: reply,
                createdAt: DateTime.now(),
              );
              setState(() {
                messages.insert(0, botMessage);
              });
            } catch (e) {
              setState(() {
                messages.insert(
                  0,
                  ChatMessage(
                    user: ChatUser(id: '2', firstName: "Assistant"),
                    text: "Error: $e",
                    createdAt: DateTime.now(),
                  ),
                );
              });
            }
          },
          messages: messages,
        ),
      ),
    );
  }
}
