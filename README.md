# Code Challenge

## The Problem
The task give was to create a service that would list the top *N* crypto assets, sorted by thei rank.
The service should expose a http endpoint which when fetched, displays an up-to-date list of top assets and their current prices in USD, in json or csv format. The endpoint should also support a limit parameter.
The ranking data and the pricing data have to be fetched from different sources.

- Ranking: https://api.coinmarketcap.com/v2/ticker/
- Pricing: https://api.coinmarketcap.com/v2/ticker/

The solutions had to be build with a service oriented architecture.


## Solution

**Note:** I used the git flow cli tool to organize my work, but it automatically deletes the branches I created, so I am not sure what you will se in the commit history. I will not merge the development branch in to master in order to preserve the commit history that I am shure is there. 
**Note 2:** Please wait a few seconds before making the first request becouse the data is still loading. The server will respond with an error message if the data is not yet ready.

### Running the solution
To run the solution run docker-compose up --build from the main folder of the project

### Main libraries used
- Flask
- Flask mqtt
- paho-mqtt
- sorted containers
- requests

### Architecture
The solution I build consists of 3 services and an mqtt broker.
The services are:
- ranking service: retrive and publish the ranking from the api
- pricing service: retrive and publish the princing list in USD
- api-gateway: collects the data published by the other two services, put it togheter and serves it

There is also a mqtt (mosquitto) broker used for comunication between the three services.
All the services user the standar mqtt port 1883, but this can be configured in the docker-compose.yml.

#### Messaging protocol
Since the service must respond with updated data, constantly polling a rest end point would be inefficient.
Also any increase on of load on the api-gateway would transfer to the other services, making scaling more expensive.
Using mqtt makes easier to constantly update the data, reducing overhead and load on the ranking and pricing services.
This solution makes scaling easier, because only the api-gateway need to be scaled if the load increses.
Using the mqtt protocol also decrease coupling between services (no client libraries must be matained across services). 

### Getting the ranking
The ranking service consists in a simple MQTT client. After connecting to the broker the service continuosly poll the ranking api, published the data the fist time, and then publish only the changes, to limit traffic.
Each ranking is published on a specific topic: 'ranking/[sybmol], eg: 'ranking/BTC'.

### Getting the prices
The pricing service is similar to the ranking service. It polls continuosly the pricing api, publish the data.
The main difference from the ranking services is that the pricing api does not return the full pricing list, but one has to iterate, making several calls offsettin the query using ghe start parameter.
Each ranking is published on a specific topic: 'pricing/[sybmol], eg: 'pricing/BTC'.

### Putting all toghether with an api gateway
The api-gateway is a simple http server created with Flask. Once running it subscribe to the pricing and ranking channels, using the wildcard '#' to collect data for all the assets.
#### Storing the rankings
Once a ranking message is received the server stores it in a sorted dictionary, using the rank as a key and the symbol of the assets as a value. Using a sorted dictionary preserve the ordering of the key, avoiding to sort the data every time is requested.
The sorted dictionary is then cached.
#### Storing the prices
Once a pricing message is received the server stores is in a dictionary using che symbol as a key and the price as value.
In this case the data is not sorted.
The pricing dictionary is the cached.

#### Creating the response
When a request is made to the endpoint, the server slices the ranking diciontary according the the limit parameter provider (if not provided defaults to 100). It then fetched the pricing data for the selected assets, using a simple dictionary to store the data. All the assets data are put in an array and returned in json form to the client. 

## Improvements
Given more time, these are the things I would improve
### Startup
All the data requires asynchronous calls, so the data is not immediatly available when the api-gateway is ready. During the startup fase more cordination between the services is needed.

### Testing
More testing to make the solution more resilient to errors  (eg: ranking or pricing api not responding, corrupted data).

### Ranking service
The ranking data does not change very often, so the constant polling of the related api is overkill. It could be transformed in to rest service that is called only when needed.

### Timestamps
It would be nice to have timestamp on the pricing data, to know how updated the prices are.

### Formats
The endpoint should accept another parameter, allowing the client to choose whic format to use (json, csv, xml).





