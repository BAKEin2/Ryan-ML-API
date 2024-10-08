const demo1App = {
    
    data() {
        return {
            inputBakeryName: "",
            inputBakeryType: "",
            inputBakeryObject:"",
            inputBakeryPrice:"",
            productList: [
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
            this.productList.push({
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
            this.productList.splice(index, 1)
        },
        editItem: function(index){
            this.productList.push({
                name: this.inputBakeryName,
                type: this.inputBakeryType,
                object : this.inputBakeryObject,
                price : this.inputBakeryPrice
            })
            this.inputBakeryName = ""
            this.inputBakeryType = ""
            this.inputBakeryObject = ""
            this.inputBakeryPrice = ""
        }
    }
}


Vue.createApp(demo1App).mount('#demo1app')