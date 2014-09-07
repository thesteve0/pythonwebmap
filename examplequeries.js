db.placenames.find({ pos : { $near :
          {
            $geometry : {
               type : "Point" ,
               coordinates : [  -122.6819 , 45.52 ]
            },           
          }
       }
    }
)


db.placenames.find({ pos : { $near :
          {
            $geometry : {
               type : "Point" ,
               coordinates : [  -122.6819 , 45.52 ]
            },
            $maxDistance : 10000
          }
       }
    }
)

db.placenames.find({FEATURE_CLASS: {$regex: 'Stream*'} ,  pos : { $near :
          {
            $geometry : {
               type : "Point" ,
               coordinates : [  -122.6819 , 45.52 ]
            },            
          }
       }} 
)

db.runCommand( { geoNear : "placenames" , near : { type : "Point" , coordinates: [  -122.6819 , 45.52] } , spherical : true, num : 10} )


db.runCommand( { geoNear : "placenames" ,
              near : { type : "Point" ,
                       coordinates: [  -122.6819 , 45.52] } ,
              spherical : true } )

