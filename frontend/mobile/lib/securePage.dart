import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:mobile/chatPage.dart';

class Securepage extends StatefulWidget {
  const Securepage({super.key});

  @override
  State<Securepage> createState() => _SecurepageState();
}

class _SecurepageState extends State<Securepage> {
  final TextEditingController _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("QueryDB"),
        centerTitle: true,
        elevation: 5,
        backgroundColor: Colors.deepOrangeAccent,
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Center(
            child: TextField(
              obscureText: true,
              controller: _controller,
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.all(Radius.circular(30)),
                ),
              ),
            ),
          ),
          SizedBox(height: 5),
          ElevatedButton(
            onPressed: () {
              print(dotenv.env["Auth"]);
              _controller.text == dotenv.env["Auth"]
                  ? Navigator.of(
                      context,
                    ).push(MaterialPageRoute(builder: (context) => ChatPage()))
                  : ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        backgroundColor: Colors.deepOrangeAccent,
                        duration: Duration(milliseconds: 1300),
                        content: Center(child: Text("Enter Correct Login Key")),
                      ),
                    );
            },
            child: Icon(Icons.verified_user),
          ),
        ],
      ),
    );
  }
}
