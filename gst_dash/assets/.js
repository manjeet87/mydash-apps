var icon_bc = L.Icon({
                    options: {
                        iconUrl: r"assets/icons/agent.png",
                        iconSize:  [10, 12],
                        iconAnchor: [10, 12]
                    }
                });
var icon_bnk = L.Icon({
                    options: {
                        iconUrl: r"assets/icons/bank.png",
                        iconSize:  [10, 10],
                        iconAnchor: [10, 10]
                    }
                });

var icon_po = L.Icon({
                    options: {
                        iconUrl: r"assets/icons/postoffice.png",
                        iconSize:  [10, 10],
                        iconAnchor: [10, 10]
                    }
                });

var icon_atm = L.Icon({
                    options: {
                        iconUrl: r"assets/icons/atms.png",
                        iconSize:  [12,10],
                        iconAnchor: [12,10]
                    }
                });


window.dash_props = Object.assign({}, window.dash_props, {
    module: {
        point_to_layer: function(feature, latlng, context) {
            return L.Marker(latlng, {icon: icon_atm})
        }
//        point_to_layer2: function(feature, latlng, context) {
//            return L.Marker(latlng, {icon: icon_po})
//        },
//        point_to_layer3: function(feature, latlng, context) {
//            return L.Marker(latlng, {icon: icon_bnk})
//        },
//        point_to_layer4: function(feature, latlng, context) {
//            return L.Marker(latlng, {icon: icon_bc})
//        }
    }
});