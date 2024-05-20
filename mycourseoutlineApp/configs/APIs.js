import axios from "axios";

const BASE_URL = 'http://10.17.64.200:8000/';

export const endpoints = {
    'categories': '/categories/',
    'lessons': '/lessons/',
    'outlines': '/outlines/'
};
export default axios.create({
    baseURL: BASE_URL
});