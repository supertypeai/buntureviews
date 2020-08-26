import React, {Component} from 'react';
import ReviewsService from './ReviewsService';

const reviewsService = new ReviewsService()

class watchlistList extends Component {

    constructor(props){
        super(props)
        this.state = {
            watchlists: []
        }
    }

    render(){
        return(
            <div className="watchlist-list">
                <table className="table">
                    <thead></thead>
                </table>
                <button className="btn btn-primary"></button>
            </div>
        )
    }

}

export default watchlistList