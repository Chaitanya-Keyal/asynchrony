const SignIn: React.FC = () => {
    return (
        <div className="flex flex-col items-center space-y-8">
            <h1 className="font-bold text-2xl text-yellow-500">SIGN IN</h1>
            <input
                type="text"
                placeholder="f20230xxx"
                className="input w-full max-w-xs"
            />
            <button className="btn btn-block bg-yellow-500 text-black hover:bg-yellow-600">Wide</button>
        </div>
    );
};

export default SignIn;
