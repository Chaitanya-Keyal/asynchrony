import { useState } from "react";
import axios from "axios";
import { useEffect, useRef } from "react";

interface Chat {
  query: String;
  response: string;
  agent?: String;
  timestamp?: String;
}

function App() {
  const [auth, setAuth] = useState<boolean>(true);

  const [message, setMessage] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const [chat, setChat] = useState<Chat[]>([]);

  const [id, setId] = useState("");

  const handleSignIn = async () => {
    try {
      const response = await axios.post("http://localhost:8000/login", {
        user_id: parseInt(id, 10),
      });

      if (parseInt(id, 10) < 1 || parseInt(id, 10) > 900) {
        alert("ID must be between 1 and 900");
        return;
      }
      setAuth(false);
      console.log(response.data.chat_history);
      setChat(response.data.chat_history);
    } catch (error) {
      console.error("Error signing in:", error);
    }
  };

  const handleSendMessage = async () => {
    setLoading(true);
    if (message.trim() === "") return;

    try {
      const response = await axios.post("http://localhost:8000/query", {
        query: message,
        user_id: parseInt(id, 10),
      });
      setChat((prevChat) => [
        ...prevChat,
        { query: message, response: response.data.response },
      ]);
      setMessage("");
    } catch (error) {
      console.error("Error sending message:", error);
    } finally {
      setLoading(false);
    }
  };

  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chat]);

  return (
    <>
      <div className="w-screen h-screen bg-gray-800 flex items-center justify-center">
        {auth ? (
          <div className="flex flex-col items-center space-y-8">
            <h1 className="font-bold text-2xl text-yellow-500">SIGN IN</h1>
            <input
              value={id}
              onChange={(e) => setId(e.target.value)}
              type="text"
              placeholder="123"
              className="input w-full max-w-xs"
            />
            <button
              onClick={handleSignIn}
              className="btn btn-block bg-yellow-500 text-black hover:bg-yellow-600"
            >
              Sign in
            </button>
          </div>
        ) : (
          <div className="p-10 bg-gray-700 shadow-2xl rounded-lg flex flex-col w-[800px] space-y-4">
            <div className="h-[500px] bg-gray-800 rounded-lg flex flex-col overflow-y-auto">
              {chat?.map((chat, index) => (
                <Message
                  key={index}
                  query={chat.query}
                  response={chat.response}
                  agent={chat.agent}
                  timestamp={chat.timestamp}
                />
              ))}
              <div ref={chatEndRef} />
            </div>

            <form
              onSubmit={(e) => e.preventDefault()}
              className="flex space-x-2"
            >
              <input
                type="text"
                placeholder="Ask any question"
                className="input w-full rounded-2xl"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
              />
              <button
                type="submit"
                onClick={handleSendMessage}
                className="btn rounded-2xl bg-yellow-500 text-black hover:bg-yellow-600"
                disabled={loading}
              >
                {loading ? "..." : "Send"}
              </button>
            </form>
          </div>
        )}
      </div>
    </>
  );
}

export default App;

const Message = (props: Chat) => {
  return (
    <>
      <div
        className={`flex space-x-2 w-full p-3 ${
          false ? "bg-gray-600" : "flex-row-reverse"
        }`}
      >
        <div className="w-10 h-10 bg-sky-700 rounded-full mx-2"></div>
        <div className="flex flex-col space-y-3 max-w-[90%]">
          <span className="font-extrabold text-sky-700 text-right">
            {false ? "Asynchrony" : "You"}
          </span>
          <p className="text-gray-300">{props.query}</p>
        </div>
      </div>
      <div
        className={`flex space-x-2 w-full p-3 ${
          true ? "bg-gray-600" : "flex-row-reverse"
        }`}
      >
        <div className="w-10 h-10 bg-emerald-600 rounded-full"></div>
        <div className="flex flex-col space-y-3 max-w-[90%]">
          <span className="font-extrabold text-emerald-500">
            {true ? "Asynchrony" : "You"}
          </span>
          <p className="text-gray-300">{props.response}</p>
        </div>
      </div>
    </>
  );
};
