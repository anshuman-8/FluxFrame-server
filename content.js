```jsx
import React from "react";

const ProfileCard = () => {
  return (
    <div className="border-2 border-blue-500 p-4 rounded-md">
      <img
        className="w-24 h-24 rounded-full mx-auto mb-4"
        src="profile-img.jpg"
        alt="Profile"
      />
      <h2 className="text-xl font-semibold">John Doe</h2>
      <p className="text-gray-500">Web Developer</p>
      <div className="flex justify-center mt-4">
        <button className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">
          View Profile
        </button>
      </div>
    </div>
  );
};

export default ProfileCard;
```