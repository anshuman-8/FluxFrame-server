const Component = () => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      {/* Post Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <div className="w-12 h-12 rounded-full bg-gray-300"></div>
          <div className="ml-3">
            <div className="w-20 h-4 bg-gray-300"></div>
            <div className="w-12 h-3 mt-1 bg-gray-300"></div>
          </div>
        </div>
        <div className="text-gray-500 cursor-pointer hover:text-black">
          <span>...</span>
        </div>
      </div>
      {/* Post Image */}
      <div className="mb-4">
        <img src="https://via.placeholder.com/400" alt="Post Image" className="rounded-lg w-full" />
      </div>
      {/* Post Actions */}
      <div className="flex justify-between mb-4">
        <div className="flex items-center space-x-4">
          <div>Love</div>
          <div>Comment</div>
          <div>Share</div>
        </div>
        <div>View 1234</div>
      </div>
      {/* Post Caption */}
      <div>
        <p className="mb-2">
          <span className="font-semibold">username</span> <span>Post Caption Post Caption Post Caption</span>
        </p>
        <p className="text-gray-500">View all 12 comments</p>
      </div>
      {/* Post Time */}
      <div className="mt-4 text-gray-500">5 hours ago</div>
    </div>
  );
}