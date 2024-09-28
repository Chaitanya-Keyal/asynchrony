import React from "react";

const Chat: React.FC = () => {
    return (
        <div className="p-10 bg-gray-700 shadow-2xl rounded-lg flex flex-col w-[800px] space-y-4">

            <div className="h-[500px] bg-gray-800 rounded-lg flex flex-col-reverse overflow-y-auto">
                <Message sender={true} />
                <Message sender={false} />
                <Message sender={true} />
                <Message sender={false} />
            </div>

            <div className="flex space-x-2">
                <input
                    type="text"
                    placeholder="Ask any question"
                    className="input w-full rounded-2xl"
                />
                <button className="btn rounded-2xl bg-yellow-500 text-black hover:bg-yellow-600">
                    Send
                </button>
            </div>
        </div>
    );
};

export default Chat;

const Message = ({sender}: {sender: boolean}) => {

    return (
        <div className={`flex space-x-2 w-full p-3 ${sender ? 'bg-gray-600' : 'flex-row-reverse' }`}>
            <div className="w-10 h-10 bg-yellow-500 rounded-full"></div>
            <div className="flex flex-col space-y-3">
                <span className="font-extrabold text-yellow-500">AI</span>
                <p className="text-gray-300">Hello</p>
            </div>
        </div>
    );
}