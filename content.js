const Component = () => {
    return (
        <div className="flex justify-center items-center h-screen">
            <div className="bg-white rounded-lg shadow-lg p-6 border-blue-500 border-2">
                <div className="flex justify-center">
                    <img className="w-24 h-24 rounded-full" src="profile-image.jpg" alt="Profile" />
                </div>
                <div className="mt-4 text-center">
                    <h2 className="text-xl font-bold">John Doe</h2>
                    <p className="text-gray-500">Software Engineer</p>
                </div>
                <div className="mt-6">
                    <p className="text-gray-500">Email: john.doe@example.com</p>
                    <p className="text-gray-500">Phone: +1 123 456 7890</p>
                    <p className="text-gray-500">Location: New York, USA</p>
                </div>
            </div>
        </div>
    );
}