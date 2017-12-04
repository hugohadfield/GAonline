
// All 4,1 canonical blade strings
var blades = {"e1":1,"e2":2,"e3":3,"e4":4,"e5":5,
"e12":6,"e13":7,"e14":8,"e15":9,"e23":10,"e24":11,"e25":12,"e34":13,"e35":14,"e45":15,
"e123":16,"e124":17,"e125":18,"e134":19,"e135":20,"e145":21,"e234":22,"e235":23,"e245":24,"e345":25,
"e1234":26,"e1235":27,"e1245":28,"e1345":29,"e2345":30,"e12345":31};

// Regex that extract the blades from the input string
var bladeRegex = /((^|\s)-?\s?\d+(\.\d+)?)\s|(-\s?\d+(\.\d+)?\^e\d+)|((^|\+)\s?\d+(\.\d+)?\^e\d)/g;

function parseMultivector(str){

    // Split the string
    var myStringArray = str.match(bladeRegex);

    // Now iterate over the array and extract the information
    var present_blades = {}
    for (var i = 0; i < myStringArray.length; i++) {
        // Trim the whitespace
        thisString = myStringArray[i].trim();
        // Split on the ^ symbol
        var stuff = thisString.split("^");
        //
        if (stuff.length === 2){
            // Extract the value of the blade and the index of the blade
            var blade_val = parseFloat(stuff[0].replace(/ /g,''));
            blade_index = blades[stuff[1].replace(/ /g,'')]
            present_blades[blade_index] = blade_val;
        }
        else{
            if(stuff.length === 1){
                // Extract the value of the scalar
                var blade_val = parseFloat(stuff[0].replace(/ /g,''));
                var blade_index = 0;
                present_blades[blade_index] = blade_val;
            }
        }
    }
    return present_blades
}

function get_sphere(present_blades){
    return $.ajax({
                url : "to_sphere/",
                type : "POST",
                data : { 'present_blades' : JSON.stringify(present_blades) } ,
            });
}

// Input string
var input_str = "-1.0 + 2.0^e1 + 1.0^e2 + 2.0^e3 - 1.0^e123";
present_blades = parseMultivector(input_str);

// Get the sphere parameters and draw it on return
get_sphere(present_blades).success(function (present_blades) {
    console.log(present_blades);
});
