var validationForHF = ee.FeatureCollection("users/MHW/HFP_Datasets/ValidationPoints_hfp"),
    HFP = ee.Image("users/MHW/hfp2000_merisINT");


    var globalRegion = ee.Geometry.Polygon(
        [[[-180, -90],
          [180, -90],
          [180, 90],
          [-180, 90],
          [-180, -90]]], 'EPSG:4326', false, 1000);

// // // ****************************************Built environments
var ISA2009 = ee.Image('users/lixuecaosysu/UrbanProduct/gUrbanTS_ISA_1km/gUrban_ISA_1km_2009')
var ISA2009_score = ee.Image(0)
          .where(ISA2009.gt(0).and(ISA2009.lt(20)), 4)
          .where(ISA2009.gte(20), 10)
          .rename('built')
Map.addLayer(ISA2009_score,{},'ISA2009_score')

// ****************************************Population density
var Pop2009 = ee.Image('users/MHW/HFP_Datasets/gWorldPOP/ppp_2009_1km_Aggregated')
// var Pop2009 = Pop2009.updateMask(Pop2009.gt(5))
var Pop2009_score = ee.Image(0)
      .where(Pop2009.gte(1000),10)
      .where(Pop2009.lt(1000), 
      Pop2009.expression('log10(img+1)*3.333', 
      {'img' : Pop2009.select('b1')})).rename('pop')
Map.addLayer(Pop2009_score,{},'Pop2009_score')

// //****************************************Night-time lights
var nt2009 = ee.Image('users/lixuecaosysu/globalNTL/stepwise_cal_DMSP/F162009v4b_webstable_lightsavg_vis')
var nt2009 = nt2009.updateMask(nt2009.gte(6))
var nt2009_score = ee.Image(0)
          .where(nt2009.gte(5).and(nt2009.lt(6)), 1)
          .where(nt2000.gte(6).and(nt2000.lt(7)), 2)
          .where(nt2000.gte(7).and(nt2000.lt(8)), 3)
          .where(nt2009.gte(8).and(nt2009.lt(9)), 4)
          .where(nt2009.gte(9).and(nt2009.lt(11)), 5)
          .where(nt2009.gte(11).and(nt2009.lt(13)), 6)
          .where(nt2009.gte(13).and(nt2009.lt(17)), 7)
          .where(nt2009.gte(17).and(nt2009.lt(24)), 8)
          .where(nt2009.gte(24).and(nt2009.lt(41)), 9)
          .where(nt2009.gte(41), 10)
          .rename('nighttime')
Map.addLayer(nt2009_score,{},'nt2009_score')

// // ****************************************ESA
var corpland2009 = ee.Image('users/MHW/gESA_cropLand/gESA_cropLand_1km_2009').selfMask()
var crop2009_score = ee.Image(0)
          .where(corpland2009.gt(0).and(corpland2009.lt(20)), 4)
          .where(corpland2009.gte(20), 10)
          .multiply(0.7)
          .rename('cropland')
// print(pasture_score)
Map.addLayer(crop2009_score,{},'crop2009_score')

// // Navigable waterways
var nav2009 = ee.Image('users/MHW/HFP_Datasets/navigableEucdistance/nav2009')
// Map.addLayer(nav2009,{},'nav2009')
var nav2009_score = nav2009.multiply(-0.001).exp().multiply(4).unmask()
.rename('navigable')
Map.addLayer(nav2009_score,{},'nav2009_score')

// // ****************************************Pasture
var pasture_score = ee.Image("users/MHW/HFP_Datasets/pastures_filled");
Map.addLayer(pasture_score,{},'pasture_score')

// Road and Railways
// var road_score = ee.Image("users/MHW/HFP_Datasets/Roads").rename('road')
var road = ee.Image("users/MHW/HFP_Datasets/roads_distance")
// Map.addLayer(road,{},'road')
var road_gte1 = ee.Image(0).where(road.gte(1),road.multiply(0.001)).selfMask()
var road_eq0 = ee.Image(0).where(road.eq(0),8)
var road_decay = road_gte1.subtract(1).multiply(-1).exp().multiply(3.75).add(0.25).unmask()
var road_score = road_eq0.add(road_decay)
Map.addLayer(road_score,{},'road_score')

var railways_score = ee.Image("users/MHW/HFP_Datasets/railways_nodata").unmask().rename('railway');
Map.addLayer(railways_score,{},'railways_score')


// // Human Footprint
var hfp2009_ord = ISA2009_score.add(Pop2009_score).add(nt2009_score).add(crop2009_score)
.add(pasture_score).add(road_score).add(railways_score).add(nav2009_score).rename('humanfootprint')

var hfp2009 = hfp2009_ord.where(hfp2009_ord.gt(50), 50).updateMask(HFP.gte(0))

Map.addLayer(hfp2009,{},'hfp2009')
Map.addLayer(HFP,{},'HFP')

// human footprint
var calccount = function(image){
  var count = image.lt(1).selfMask().reduceRegion({
    // var count = image.reduceRegion({
    geometry: globalRegion, //改这里 
    reducer: ee.Reducer.count(),
    scale: 1000,
    maxPixels: 10e13,
});
return ee.Feature(null,{'area':count.getNumber('humanfootprint')})
}
var hfps = ee.ImageCollection([hfp2009])
Map.addLayer(hfps.first())
print(hfps)
var hfpsList = hfps.map(calccount)
print(hfpsList)


var hfp2009_validation = hfp2009.sampleRegions({
  collection:validationForHF,
  scale: 1000, 
  tileScale:4
})
// print(hfp2009_validation)
// Map.addLayer(validationForHF)

Export.table.toDrive({
  collection: hfp2009_validation.map(function(feature){return feature.setGeometry(null)}),
  description:'hfp_validation', ////”/////////////////改这里
  folder:'HumanFootprint',
  fileFormat: 'CSV'
})

Export.image.toAsset({
  image: hfp2009.set(({'year':2009})),
  description:'hfp2009',
  assetId:'users/MHW/HFP_Datasets/humanfootprintG/hfp2009',
  scale:1000,
  region: HFP.geometry(),
  maxPixels:1e13
});

// https://code.earthengine.google.com/bce7cc6c36259a5490a289630151cffb?noload=1