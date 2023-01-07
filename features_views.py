import hsfs
import hopsworks
#RvLmP6cByDVIO2do.eUiPUAajvVgkNKBoBKswguvGuCb3UvWY9lnuw832q5mYKbC5eD4en9QbdsntpyDq


project = hopsworks.login()
fs = project.get_feature_store() 

air_columns_names = ['city', 'aqi', 'iaqi_h', 'iaqi_p', 'iaqi_pm10', 'iaqi_t', 'date',
                'o3_avg', 'o3_max', 'o3_min', 'pm10_avg', 'pm10_max', 'pm10_min',
                'pm25_avg', 'pm25_max', 'pm25_min']



air_quality_fg = fs.get_or_create_feature_group(
    name = 'air_quality_fg',
    version = 1
)
weather_fg = fs.get_or_create_feature_group(
    name = 'weather_fg',
    version = 1
)

query = air_quality_fg.select_all().join(weather_fg.select_all(), on=['city', 'date'])

air_columns = air_quality_fg.select_all().show(5).columns
weather_columns = weather_fg.select_all().show(5).columns

col_names = list(air_columns) + list(weather_columns)

category_cols = ['city','date','conditions','aqi']
mapping_transformers = {col_name:fs.get_transformation_function(name='standard_scaler') for col_name in col_names if col_name not in category_cols}
category_cols = {col_name:fs.get_transformation_function(name='label_encoder') for col_name in category_cols if col_name not in ['date','aqi']}
mapping_transformers.update(category_cols)


feature_view = fs.create_feature_view(
    name = 'air_quality_fv',
    version = 1,
    transformation_functions = mapping_transformers,
    query = query
)

feature_view = fs.get_feature_view(
    name = 'air_quality_fv',
    version = 1
)