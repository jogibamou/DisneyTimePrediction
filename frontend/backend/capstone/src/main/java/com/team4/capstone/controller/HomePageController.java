package com.team4.capstone.controller;

import com.google.gson.JsonObject;
import com.team4.capstone.dto.WaitTimeRequestDto;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
@RestController
public class HomePageController {

    @PostMapping(value = "/predict", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<String> predict(@RequestBody WaitTimeRequestDto waitTimeDetails){
        System.out.println(waitTimeDetails.toString());
        RestTemplate restTemplate = new RestTemplate();
        HttpEntity<String> request = new HttpEntity<>(makeJson(waitTimeDetails).toString());
        String response = restTemplate.postForObject("URL", request, String.class);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    private JsonObject makeJson(WaitTimeRequestDto timeDetails){
        JsonObject requestDetails = new JsonObject();
        requestDetails.addProperty("DateTime", timeDetails.getDateTime());
        requestDetails.addProperty("Park", timeDetails.getPark());
        requestDetails.addProperty("Ride", timeDetails.getRide());
        return requestDetails;
    }
}
