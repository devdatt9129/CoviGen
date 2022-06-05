const express=require('express');
const mysql=require('mysql');
var bodyParser=require('body-parser');
const morgan = require('morgan');

const app=express();
app.use(express.json());
app.use(express.urlencoded({extended:false}));
app.use("/",express.static(__dirname + '/'));
app.use(morgan('short'));


var connection=mysql.createConnection({
    host:"localhost",
    user:"root",
    password:"Redemption9129@123",
    database:"final_db",
    port:"3306"
})
connection.connect((err)=>{
    if(err){
        console.log('Not connected');
    }
    else{
        console.log("connected");
    }
})

/*app.post('/user_create', (req, res) => {

    console.log("Trying to create a new user...")
    console.log("How do we get the form data???")

   // console.log("First name: " + req.body.create_first_name)
    //const firstName = req.body.create_first_name
    //const lastName = req.body.create_last_name

    const queryString = "'INSERT INTO coviddb(id,name,age,result) VALUES(?,?,?,?)"
    connection.query(queryString, [firstName, lastName], (err, results, fields) => {
      if (err) {
        console.log("Failed to insert new user: " + err)
        res.sendStatus(500)
        return
      }
    
      console.log("Inserted a new user with id: ", results.insertId);
      res.end()
    })
    })
connection.query('INSERT INTO coviddb(id,name,age,result) VALUES(?,?,?,?)',[999,"rod",12,"Covid Positive"],(err,rows) =>{
    if(err){
        console.log('Not connected');
    }
    else{
        console.log('Data queried');
        console.log(rows);
    }
} )*/

/*app.get("/",(req,res)=>{
    console.log('Responding to the root route ');
    res.send('Hello from root');
})*/
const port =process.env.port || 5000;
app.listen(port);
console.log("app is listening on port"+port);
