const demo1App = {
    
    data() {
        return {
            inputBakeryName: "",
            inputBakeryType: "",
            inputBakeryObject:"",
            inputBakeryPrice:"",
            cartList: [
                {
                    name: "BreadTalk",
                    type: "Muffins",
                    object: "Chocolate Muffin",
                    price: "10.00"
                },
                {
                    name: "Swee Heng",
                    type: "Cupcakes",
                    object: "Strawberry Cupcake",
                    price: "8.00"
                }
            ]
        }
    }, 
    methods: {
        addNewItem: function() {
            this.cartList.push({
                name: this.inputBakeryName,
                type: this.inputBakeryType,
                object : this.inputBakeryObject,
                price : this.inputBakeryPrice
            })
            this.inputBakeryName = ""
            this.inputBakeryType = ""
            this.inputBakeryObject = ""
            this.inputBakeryPrice = ""
        },
        deleteItem: function(index) {
            this.cartList.splice(index, 1)
        }
    }
}


Vue.createApp(demo1App).mount('#demo1app')