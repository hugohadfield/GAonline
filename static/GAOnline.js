


/* 
This section of the code deals with parseing text input from the user
*/

// All 4,1 canonical blade strings
var blades = {"e1":1,"e2":2,"e3":3,"e4":4,"e5":5,
"e12":6,"e13":7,"e14":8,"e15":9,"e23":10,"e24":11,"e25":12,"e34":13,"e35":14,"e45":15,
"e123":16,"e124":17,"e125":18,"e134":19,"e135":20,"e145":21,"e234":22,"e235":23,"e245":24,"e345":25,
"e1234":26,"e1235":27,"e1245":28,"e1345":29,"e2345":30,"e12345":31};

// Regex that extract the blades from the input string
var bladeRegex = /((^|\s)-?\s?\d+(\.\d+)?)\s|(-\s?(\d+((e(\+|-))|\.)?(\d+)?)\^e\d+(\s|$))|((^|\+)\s?(\d+((e(\+|-))|\.)?(\d+)?)\^e\d+(\s|$))/g;

function parseMultivector(str){

    // Split the string
    str = str.replace(/[()]/g, "");
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

function callFunction(funcName,mvString,colorString,scene){
    var present_blades = parseMultivector(mvString);
    window[funcName](present_blades,colorString,scene);
}

// Regex that extracts the functions with their arguments
var functionRegex = /\w+\(.+\);/g;

function parseScriptToFunctions(str,scene){
    var myStringArray = str.match(functionRegex);
    for (var i = 0; i < myStringArray.length; i++) {
        var thisFunctionString = myStringArray[i];
        // Get the function name
        var funcName = thisFunctionString.split(/\(/,1)[0];
        console.log(funcName);

        // Get the arguments to the function as a string
        var mvArg = thisFunctionString.slice(funcName.length+1,-2);
        console.log(mvArg);

        // Split the argument string on the first comma which comes immediately after the multivector
        var mvString = mvArg.split(/,/,1)[0];
        console.log(mvString);

        var colorString = mvArg.slice(mvString.length+1);
        console.log(colorString);

        // Call the function with the relevant arguments
        callFunction(funcName,mvString,colorString,scene);
    }
}

function get_point_pair(present_blades){
    return $.ajax({
                url : "to_point_pair/",
                type : "POST",
                data : { 'present_blades' : JSON.stringify(present_blades) } ,
            });
}

function get_sphere(present_blades){
    return $.ajax({
                url : "to_sphere/",
                type : "POST",
                data : { 'present_blades' : JSON.stringify(present_blades) } ,
            });
}

function get_plane(present_blades){
    return $.ajax({
                url : "to_plane/",
                type : "POST",
                data : { 'present_blades' : JSON.stringify(present_blades) } ,
            });
}

function get_line(present_blades){
    return $.ajax({
                url : "to_line/",
                type : "POST",
                data : { 'present_blades' : JSON.stringify(present_blades) } ,
            });
}

function get_circle(present_blades){
    return $.ajax({
                url : "to_circle/",
                type : "POST",
                data : { 'present_blades' : JSON.stringify(present_blades) } ,
            });
}

/*
This section creates the scene and axes
*/

function buildAxis( src, dst, colorHex, dashed ) {
    var geom = new THREE.Geometry(),
        mat;
    if(dashed) {
            mat = new THREE.LineDashedMaterial({ linewidth: 3, color: colorHex, dashSize: 3, gapSize: 3 });
    } else {
            mat = new THREE.LineBasicMaterial({ linewidth: 3, color: colorHex, transparent: true, opacity:0.2  });
    }
    geom.vertices.push( src.clone() );
    geom.vertices.push( dst.clone() );
    geom.computeLineDistances(); // This one is SUPER important, otherwise dashed lines will appear as simple plain lines
    var axis = new THREE.Line( geom, mat, THREE.LinePieces );
    return axis;
}

function buildAxes( length ) {
    var axes = new THREE.Object3D();
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( length, 0, 0 ), 0xFF0000, false ) ); // +X
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( -length, 0, 0 ), 0xFF0000, false) ); // -X
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( 0, length, 0 ), 0x00FF00, false ) ); // +Y
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( 0, -length, 0 ), 0x00FF00, false ) ); // -Y
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( 0, 0, length ), 0x0000FF, false ) ); // +Z
    axes.add( buildAxis( new THREE.Vector3( 0, 0, 0 ), new THREE.Vector3( 0, 0, -length ), 0x0000FF, false ) ); // -Z
    return axes;
}

function MapToAxisSystem(vectorin){
    return [vectorin[0],vectorin[1],vectorin[2]];
}


function DrawPointPair(present_blades,draw_color,scene){
    get_point_pair(present_blades).success(function (returned_data) {
        console.log(returned_data);
        var a = returned_data.a;
        var b = returned_data.b;
        
        var radius = 0.05;
        var geometry = new THREE.SphereGeometry( radius, 32, 32 );
        var material = new THREE.MeshBasicMaterial( {color: draw_color, wireframe: false} );
        var sphere_a = new THREE.Mesh( geometry, material );
        sphere_a.position.set(a[0],a[1],a[2])
        scene.add(sphere_a);

        var material = new THREE.MeshBasicMaterial( {color: draw_color, wireframe: false} );
        var sphere_b = new THREE.Mesh( geometry, material );
        sphere_b.position.set(b[0],b[1],b[2])
        scene.add(sphere_b);

        var line_width = parseFloat(document.getElementById("linewidthArea").value);

        var material = new THREE.LineBasicMaterial({
            color: draw_color,
            linewidth : line_width
        });

        var a_pos = new THREE.Vector3( a[0],a[1],a[2] )
        var b_pos = new THREE.Vector3( b[0],b[1],b[2] )
        var geometry = new THREE.Geometry();
        geometry.vertices.push(
            a_pos,
            b_pos
        );
        var line = new THREE.Line( geometry, material );
        scene.add( line );

        var geometry = new THREE.ConeGeometry( 2*radius, radius*4, 6 );
        var material = new THREE.MeshBasicMaterial( {color: draw_color, wireframe: false} );
        var cone = new THREE.Mesh( geometry, material );
        var c_pos = a_pos.clone();
        c_pos.add( b_pos ).multiplyScalar(0.5);

        var axis = new THREE.Vector3(0, 1, 0);
        cone.quaternion.setFromUnitVectors(axis, b_pos.clone().sub(a_pos).normalize());
        cone.position.set( c_pos.x, c_pos.y, c_pos.z );
        scene.add( cone );

    });
}


function DrawEucPoint(present_blades,draw_color,scene){
    var radius = 0.05;
    var geometry = new THREE.SphereGeometry( radius, 32, 32 );
    var material = new THREE.MeshBasicMaterial( {color: draw_color, wireframe: false} );
    var sphere = new THREE.Mesh( geometry, material );

    var a = present_blades[1]
    var b = present_blades[2]
    var c = present_blades[3]

    if (typeof(a) === "undefined") {a = 0.0;};
    if (typeof(b) === "undefined") {b = 0.0;};
    if (typeof(c) === "undefined") {c = 0.0;};

    sphere.position.set(a,b,c)
    scene.add(sphere);
}


function DrawSphere(present_blades,draw_color,scene){
    // Get the sphere parameters and draw it on return
    get_sphere(present_blades).success(function (returned_data) {
        console.log(returned_data);
        var centre = MapToAxisSystem(returned_data.centre);
        var radius = returned_data.radius;
        var geometry = new THREE.SphereGeometry( radius, 64, 64 );
        var material = new THREE.MeshBasicMaterial( {color: draw_color, wireframe: false, transparent: true, 
            opacity: 0.1,
            side: THREE.DoubleSide, 
            depthWrite: false} );
        var sphere = new THREE.Mesh( geometry, material );

        var material2 = new THREE.MeshBasicMaterial( {color: draw_color, wireframe: true, transparent: true, opacity: 0.05} );
        var sphere2 = new THREE.Mesh( geometry, material2 );
        sphere.position.set(centre[0],centre[1],centre[2])
        sphere2.position.set(centre[0],centre[1],centre[2])
        scene.add(sphere);
        scene.add(sphere2);
    });
}

function DrawPlane(present_blades,draw_color,scene){
    // Get the sphere parameters and draw it on return
    get_plane(present_blades).success(function (returned_data) {
        console.log(returned_data);
        var distance = returned_data.distance;
        var normal = MapToAxisSystem(returned_data.normal);
        var position = [normal[0]*distance,normal[1]*distance,normal[2]*distance];
        
        // Add a floor
        var geometry = new THREE.PlaneGeometry( 100, 100, 100, 100 );
        var material = new THREE.MeshBasicMaterial( { color: draw_color, wireframe: false,
        transparent: true, 
            opacity: 0.5,
            side: THREE.DoubleSide, 
            depthWrite: false} );
        var plane = new THREE.Mesh( geometry, material );
        plane.material.side = THREE.DoubleSide;
        plane.lookAt(normal[0],normal[1],normal[2]);
        plane.position.set(position[0],position[1],position[2]);
        scene.add( plane );

        var material = new THREE.MeshBasicMaterial( { color: draw_color, wireframe: true} );
        var plane = new THREE.Mesh( geometry, material );
        plane.material.side = THREE.DoubleSide;
        plane.lookAt(normal[0],normal[1],normal[2]);
        plane.position.set(position[0],position[1],position[2]);
        scene.add( plane );
    });
}


function DrawLine(present_blades,draw_color,scene){
    get_line(present_blades).success(function (returned_data) {
        console.log(returned_data);
        var direction = MapToAxisSystem(returned_data.direction);
        var point = MapToAxisSystem(returned_data.point);

        var line_width = parseFloat(document.getElementById("linewidthArea").value);
        
        var material = new THREE.LineBasicMaterial({
            color: draw_color,
            linewidth : line_width
        });
        var geometry = new THREE.Geometry();
        geometry.vertices.push(
            new THREE.Vector3( point[0]+500*direction[0], point[1]+500*direction[1], point[2]+500*direction[2] ),
            new THREE.Vector3( point[0]-500*direction[0], point[1]-500*direction[1], point[2]-500*direction[2] )
        );
        var line = new THREE.Line( geometry, material );
        scene.add( line );
    });
}

function DrawCircle(present_blades,draw_color,scene){
    get_circle(present_blades).success(function (returned_data) {
        console.log(returned_data);
        var radius = abs(returned_data.radius);
        var centre = MapToAxisSystem(returned_data.centre);
        var normal = MapToAxisSystem(returned_data.normal);
        var imaginary = (returned_data.radius < 0);
        // Not sure what to do in the case that we have an imaginary circle
        // Probably should draw it in a dashed way
        var geometry = new THREE.TorusGeometry( radius, 0.05, 16,32 );
        var material = new THREE.MeshBasicMaterial( { color: draw_color } );
        var torus = new THREE.Mesh( geometry, material );
        torus.lookAt(normal[0],normal[1],normal[2]);
        torus.position.set(centre[0],centre[1],centre[2]);
        scene.add( torus );
    });
}


// Set up the scene and window size
var scene = new THREE.Scene();
var canvas_width = window.innerWidth;
var canvas_height = window.innerHeight;

// Create a camera object
var camera = new THREE.PerspectiveCamera( 75, canvas_width/canvas_height, 0.1, 1000 );

// Set up orbit controls
container = document.getElementById( 'scene3d' );

function ResetCamera(){
    camera.position.set( 5, 0, 5 );
    camera.up.set( 0, 0, 1 );
}

function ResetControls(){
    controls.target = new THREE.Vector3();
}

ResetCamera();

var controls = new THREE.OrbitControls( camera, container );
controls.update();

function ZoomIn(){
    controls.dollyIn(1.1);
}

function ZoomOut(){
    controls.dollyOut(1.1);
}

function CenterViewBtn(){
    ResetCamera();
    ResetControls();
};

CenterViewBtn();


// Create a renderer and add it to the DOM
var renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize( canvas_width, canvas_height);
container.appendChild( renderer.domElement );

var scriptLines = "";
var ANIMATION_RUNNING = false;
function AnimateUserScript(frameRate, frameCounter, init){
    if (ANIMATION_RUNNING == true) {
        if (init == true){
            return 1
        }
    }
    console.log(frameCounter);
    if (frameCounter == 0){
        scriptLines = document.getElementById("scriptTextArea").value.split('\n');
        ANIMATION_RUNNING = true;
    }
    if (frameCounter < scriptLines.length){
        var input_str = scriptLines[frameCounter].replace(/#/g, "\n")
        // Clear the scene
        var draw_axes = document.getElementById("axesCheck").checked;
        resetScene(scene,draw_axes);
        // Add the new stuff
        parseScriptToFunctions(input_str,scene);
        window.setTimeout(function() {AnimateUserScript(frameRate, frameCounter+1, false)}, 1000.0/(frameRate))
    }
    else{
        ANIMATION_RUNNING = false;
    }
}


// Do the things
function ParseUserScript(){
    // Get the input string
    var input_str = document.getElementById("scriptTextArea").value;
    // Clear the scene
    var draw_axes = document.getElementById("axesCheck").checked;
    resetScene(scene,draw_axes);
    // Add the new stuff
    parseScriptToFunctions(input_str,scene);
}

// Add a floor
var ground_geometry = new THREE.PlaneGeometry( 100, 100, 100, 100 );
var ground_material = new THREE.MeshBasicMaterial( { color: 0x0000ff, wireframe: true, transparent: true, opacity: 0.2} );
var ground_plane = new THREE.Mesh( ground_geometry, ground_material );
var global_axes = buildAxes( 1000 ); 

ParseUserScript();


function resetScene(scene, floor_and_axes_bool){
    // Remove everything from the scene first
    for (let i = scene.children.length - 1; i >= 0; i--) {
        scene.remove(scene.children[i]);
    }
    if (floor_and_axes_bool){
        // Build coordinate axes
        scene.add(global_axes);
        scene.add(ground_plane);
    }
}

// Animate the scene
var animate = function () {
    requestAnimationFrame( animate );
    // required if controls.enableDamping or controls.autoRotate are set to true
    controls.update();
    renderer.render(scene, camera);
};
animate();

