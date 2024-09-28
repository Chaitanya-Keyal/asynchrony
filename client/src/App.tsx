import SignIn from "./SignIn";
import Chat from "./Chat";

function App() {

  const auth: boolean = false;

  return (
    <>
      <div className="w-screen h-screen bg-gray-800 flex items-center justify-center">
        {auth ? (
          <SignIn></SignIn>
        ) : (
          <Chat></Chat>
        )}
      </div>
    </>
  )
}

export default App
