const Component = () => {
  return (
    <div className="flex flex-col bg-white rounded-md shadow-lg p-4">
      <div className="flex items-center">
        <img
          src="https://picsum.photos/50"
          alt="Profile Picture"
          className="w-10 h-10 rounded-full"
        />
        <div className="flex flex-col ml-2">
          <span className="font-bold text-lg">Username</span>
          <span className="text-gray-500 text-sm">Location</span>
        </div>
      </div>

      <img
        src="https://picsum.photos/400"
        alt="Post"
        className="my-4 rounded-md w-full"
      />

      <div className="flex">
        <button className="flex items-center mr-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
          <span className="ml-2">Like</span>
        </button>
        <button className="flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M16 19l-1.1-5.1M8 19l1.1-5.1"
            />
          </svg>
          <span className="ml-2">Comment</span>
        </button>
      </div>
    </div>
  );
};