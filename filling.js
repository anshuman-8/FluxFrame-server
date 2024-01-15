const Component = () => {
  return (
    <div className="flex flex-col items-center justify-center">
      
        <div className="bg-gray-100 rounded-full h-32 w-32 flex items-center justify-center border-4 border-red-500">
            <img
                src="profile_picture.jpg"
                alt="Profile Picture"
                className="rounded-full h-28 w-28"
            />
        </div>
      
      <div className="mt-4 text-center">
        <h2 className="text-2xl font-bold">John Doe</h2>
        <p className="text-gray-500">Date of Birth: 01/01/1990</p>
      </div>
    </div>
  );
};
</Component>