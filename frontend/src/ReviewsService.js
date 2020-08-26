import axios from 'axios';
const API_URL = 'http://localhost:8000/api/v1';

export default class ReviewsService {
    constructor(){}

    getWatchList(){
        const url = `${API_URL}/watch-lists/`
        return axios.get(url).then(response => response.data)
    }

}