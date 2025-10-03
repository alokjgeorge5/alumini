import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is admin
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || user.role !== 'admin') {
      navigate('/login');
      return;
    }
    setCurrentUser(user);
    fetchUsers();
  }, [navigate]);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE_URL}/admin/users`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data);
    } catch (error) {
      toast.error('Failed to fetch users');
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`${API_BASE_URL}/admin/users/${userId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('User deleted successfully');
        fetchUsers();
      } catch (error) {
        toast.error('Failed to delete user');
        console.error('Error deleting user:', error);
      }
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>
      
      <div className="bg-white shadow-md rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Users Management</h2>
        
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white">
            <thead>
              <tr className="bg-gray-100">
                <th className="py-2 px-4 border-b border-gray-200 text-left">Name</th>
                <th className="py-2 px-4 border-b border-gray-200 text-left">Email</th>
                <th className="py-2 px-4 border-b border-gray-200 text-left">Role</th>
                <th className="py-2 px-4 border-b border-gray-200 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="py-3 px-4 border-b border-gray-200">{user.name}</td>
                  <td className="py-3 px-4 border-b border-gray-200">{user.email}</td>
                  <td className="py-3 px-4 border-b border-gray-200 capitalize">{user.role}</td>
                  <td className="py-3 px-4 border-b border-gray-200 text-right">
                    {user.id !== currentUser.id && (
                      <button
                        onClick={() => handleDeleteUser(user.id)}
                        className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
