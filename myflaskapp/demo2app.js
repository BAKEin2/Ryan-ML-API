const demo2App = {
    
    data() {
        return {
            longitude: "",
            latitude: "",
            bread_interests: "",
            userID: "",
            rating : "",
            placeID : "",
            userID_rating: "",
        }
    }, 
    methods: {
        predictPopularBakeries: function() {
            console.log(JSON.stringify(
                {
                    longitude: this.longitude,
                    latitude: this.latitude,
                }
            ))
            fetch('http://127.0.0.1:5000/recommendPopularBakeries', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },                
                body: JSON.stringify(
                    {
                        longitude: parseFloat(this.longitude),
                        latitude: parseFloat(this.latitude),
                    }
                )
            })
            .then(response => response.json())
            .then(result => {
                alert(result.result)
            })
            .catch(error => {
                console.error('Error:', error);
            });            
        },
        predictInterestBakeries: function() {
            console.log(JSON.stringify(
                {
                    longitude: this.longitude,
                    latitude: this.latitude,
                    bread_interests : this.bread_interests
                }
            ))
            fetch('http://127.0.0.1:5000/recommendInterestBakeries', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },                
                body: JSON.stringify(
                    {
                        longitude: parseFloat(this.longitude),
                        latitude: parseFloat(this.latitude),
                        bread_interests: String(this.bread_interests),
                    }
                )
            })
            .then(response => response.json())
            .then(result => {
                alert(result.result)
            })
            .catch(error => {
                console.error('Error:', error);
            });            
        },
        predictRatedBakeries: function() {
            console.log(JSON.stringify(
                {
                    userID: this.userID,
                    rating: this.rating,
                    placeID: this.placeID,
                    userID_rating: this.userID_rating,
                }
            ))
            fetch('http://127.0.0.1:5000/recommendRatedBakeries', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },                
                body: JSON.stringify(
                    {
                        userID: parseInt(this.userID),
                        rating: parseInt(this.rating),
                        placeID: parseInt(this.placeID),
                        userID_rating: parseInt(this.userID_rating),
                    }
                )
            })
            .then(response => response.json())
            .then(result => {
                alert(result.result)
            })
            .catch(error => {
                console.error('Error:', error);
            });            
        }
    }
}


Vue.createApp(demo2App).mount('#demo2app')