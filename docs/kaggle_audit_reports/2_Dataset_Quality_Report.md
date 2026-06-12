# Dataset Quality Report

## Egypt Datasets Comparison
| Dataset | Records | Columns | Missing % | Duplicates % |
|---|---|---|---|---|

### Overlap Analysis

## All Datasets
### audit_results.json (`audit_results.json`)
- **Size**: 382.39 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### sample_100.csv (`cmt_test\datasets\sample_100.csv`)
- **Size**: 9.31 KB
- **Records**: 100
- **Columns**: 10
- **Missing %**: 4.20%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52968090', 'price': '50000', 'property_type': 'iVilla', 'compound': 'nan', 'area': 'Mountain View Executive', 'bedrooms': '3.0', 'bathrooms': '3', 'size_sqm': '300.0', 'lat': '29.99061...`

### sample_250.csv (`cmt_test\datasets\sample_250.csv`)
- **Size**: 22.90 KB
- **Records**: 250
- **Columns**: 10
- **Missing %**: 4.76%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52968090', 'price': '50000', 'property_type': 'iVilla', 'compound': 'nan', 'area': 'Mountain View Executive', 'bedrooms': '3.0', 'bathrooms': '3', 'size_sqm': '300.0', 'lat': '29.99061...`

### sample_500.csv (`cmt_test\datasets\sample_500.csv`)
- **Size**: 46.01 KB
- **Records**: 500
- **Columns**: 10
- **Missing %**: 4.80%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52968090', 'price': '50000', 'property_type': 'iVilla', 'compound': 'nan', 'area': 'Mountain View Executive', 'bedrooms': '3.0', 'bathrooms': '3', 'size_sqm': '300.0', 'lat': '29.99061...`

### sample_dry_run.csv (`cmt_test\datasets\sample_dry_run.csv`)
- **Size**: 535.00 B
- **Records**: 5
- **Columns**: 10
- **Missing %**: 6.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52968090', 'price': '50000', 'property_type': 'iVilla', 'compound': 'nan', 'area': 'Mountain View Executive', 'bedrooms': '3', 'bathrooms': '3', 'size_sqm': '300.0', 'lat': '29.9906158...`

### comps_count_analysis.csv (`cmt_test\metrics\comps_count_analysis.csv`)
- **Size**: 327.00 B
- **Records**: 6
- **Columns**: 4
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'Comps Count Bucket': '1-5 comps', 'Count': '18', 'MAPE': '1.0', 'Median Error': '1.0'}...`

### confidence_validation.csv (`cmt_test\metrics\confidence_validation.csv`)
- **Size**: 265.00 B
- **Records**: 5
- **Columns**: 4
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'Confidence Bucket': '0.0-0.2', 'Count': '0', 'MAPE': '1.0', 'Median Error': '1.0'}...`

### segment_analysis.csv (`cmt_test\metrics\segment_analysis.csv`)
- **Size**: 12.22 KB
- **Records**: 174
- **Columns**: 7
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'Segment Type': 'Governorate', 'Segment Value': 'Alexandria', 'Count': '2', 'MAPE': '0.1666666666666666', 'Median Error': '0.1666666666666666', 'Within 10%': '0.0', 'Within 20%': '0.5'}...`

### summary_metrics.csv (`cmt_test\metrics\summary_metrics.csv`)
- **Size**: 511.00 B
- **Records**: 3
- **Columns**: 13
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'Dataset': '100 sample', 'Count': '100', 'Failed Count': '14', 'MAPE (Mean)': '0.2703302384383219', 'MAPE (Median)': '0.1666666666666666', 'RMSE': '31942.44751930033', 'MAE': '17879.058139534885', 'R...`

### tier_analysis.csv (`cmt_test\metrics\tier_analysis.csv`)
- **Size**: 235.00 B
- **Records**: 5
- **Columns**: 4
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'Tier Used': '1.0', 'Count': '148.0', 'MAPE': '0.2120018840688316', 'Median Error': '0.1538461538461538'}...`

### results_100.csv (`cmt_test\raw_results\results_100.csv`)
- **Size**: 6.15 KB
- **Records**: 100
- **Columns**: 8
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52968090.0', 'actual_price': '50000.0', 'predicted_price': '75000.0', 'error_pct': '0.5', 'confidence': '0.8470969872614242', 'tier_used': '3.0', 'comps_count': '86.0', 'execution_time...`

### results_250.csv (`cmt_test\raw_results\results_250.csv`)
- **Size**: 14.39 KB
- **Records**: 250
- **Columns**: 8
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52968090.0', 'actual_price': '50000.0', 'predicted_price': '75000.0', 'error_pct': '0.5', 'confidence': '0.8470969872614242', 'tier_used': '3.0', 'comps_count': '86.0', 'execution_time...`

### results_500.csv (`cmt_test\raw_results\results_500.csv`)
- **Size**: 29.02 KB
- **Records**: 500
- **Columns**: 8
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52968090.0', 'actual_price': '50000.0', 'predicted_price': '75000.0', 'error_pct': '0.5', 'confidence': '0.8470969872614242', 'tier_used': '3.0', 'comps_count': '86.0', 'execution_time...`

### results_dry_run.csv (`cmt_test\raw_results\results_dry_run.csv`)
- **Size**: 431.00 B
- **Records**: 5
- **Columns**: 8
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52968090.0', 'actual_price': '50000.0', 'predicted_price': '75000.0', 'error_pct': '0.5', 'confidence': '0.8470969872614242', 'tier_used': '3.0', 'comps_count': '86.0', 'execution_time...`

### firebase.json (`flutter_valorai\firebase.json`)
- **Size**: 527.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'flutter': "{'android': {'default': {'projectId': 'valorai-e25b8', 'appId': '1:11968174472:android:2cc2db96b6d45da81b023d', 'fileOutput': 'android/app/google-services.json'}}, 'dart': {'lib/firebase_...`

### package_config.json (`flutter_valorai\.dart_tool\package_config.json`)
- **Size**: 23.22 KB
- **Records**: 113
- **Columns**: 7
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'configVersion': '2', 'packages': "{'name': '_flutterfire_internals', 'rootUri': 'file:///C:/Users/mh978/AppData/Local/Pub/Cache/hosted/pub.dev/_flutterfire_internals-1.3.72', 'packageUri': 'lib/', '...`

### package_graph.json (`flutter_valorai\.dart_tool\package_graph.json`)
- **Size**: 20.07 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### dart_build_result.json (`flutter_valorai\.dart_tool\flutter_build\8215958b7c3cedc50c82589e95132e80\dart_build_result.json`)
- **Size**: 521.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### native_assets.json (`flutter_valorai\.dart_tool\flutter_build\8215958b7c3cedc50c82589e95132e80\native_assets.json`)
- **Size**: 45.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### outputs.json (`flutter_valorai\.dart_tool\flutter_build\8215958b7c3cedc50c82589e95132e80\outputs.json`)
- **Size**: 1.69 KB
- **Records**: 11
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'0': 'C:\\Users\\mh978\\Downloads\\mobile computing project\\flutter_valorai\\build\\app\\intermediates\\flutter\\debug\\flutter_assets\\vm_snapshot_data'}...`

### dart_build_result.json (`flutter_valorai\.dart_tool\flutter_build\8523b181f773a335aec3241355e927a8\dart_build_result.json`)
- **Size**: 521.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### native_assets.json (`flutter_valorai\.dart_tool\flutter_build\8523b181f773a335aec3241355e927a8\native_assets.json`)
- **Size**: 45.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### outputs.json (`flutter_valorai\.dart_tool\flutter_build\8523b181f773a335aec3241355e927a8\outputs.json`)
- **Size**: 1.67 KB
- **Records**: 11
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'0': 'C:\\Users\\mh978\\Downloads\\mobile computing project\\flutter_valorai\\build\\app\\intermediates\\flutter\\release\\flutter_assets\\packages\\cupertino_icons\\assets\\CupertinoIcons.ttf'}...`

### dependencies.dependencies_hash_file.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\365da55a17\dependencies.dependencies_hash_file.json`)
- **Size**: 400.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### hook.dependencies_hash_file.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\365da55a17\hook.dependencies_hash_file.json`)
- **Size**: 425.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### input.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\365da55a17\input.json`)
- **Size**: 1.26 KB
- **Records**: 3
- **Columns**: 7
- **Missing %**: 28.57%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'assets': 'nan', 'config': "['code_assets/code']", 'out_dir_shared': 'C:\\Users\\mh978\\Downloads\\mobile computing project\\flutter_valorai\\.dart_tool\\hooks_runner\\shared\\objective_c\\build\\', ...`

### output.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\365da55a17\output.json`)
- **Size**: 95.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### dependencies.dependencies_hash_file.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\397cf31330\dependencies.dependencies_hash_file.json`)
- **Size**: 400.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### hook.dependencies_hash_file.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\397cf31330\hook.dependencies_hash_file.json`)
- **Size**: 425.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### input.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\397cf31330\input.json`)
- **Size**: 1.26 KB
- **Records**: 3
- **Columns**: 7
- **Missing %**: 28.57%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'assets': 'nan', 'config': "['code_assets/code']", 'out_dir_shared': 'C:\\Users\\mh978\\Downloads\\mobile computing project\\flutter_valorai\\.dart_tool\\hooks_runner\\shared\\objective_c\\build\\', ...`

### output.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\397cf31330\output.json`)
- **Size**: 95.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### dependencies.dependencies_hash_file.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\6441582121\dependencies.dependencies_hash_file.json`)
- **Size**: 400.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### hook.dependencies_hash_file.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\6441582121\hook.dependencies_hash_file.json`)
- **Size**: 425.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### input.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\6441582121\input.json`)
- **Size**: 1.26 KB
- **Records**: 3
- **Columns**: 7
- **Missing %**: 28.57%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'assets': 'nan', 'config': "['code_assets/code']", 'out_dir_shared': 'C:\\Users\\mh978\\Downloads\\mobile computing project\\flutter_valorai\\.dart_tool\\hooks_runner\\shared\\objective_c\\build\\', ...`

### output.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\6441582121\output.json`)
- **Size**: 95.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### dependencies.dependencies_hash_file.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\8e04c28b44\dependencies.dependencies_hash_file.json`)
- **Size**: 398.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### hook.dependencies_hash_file.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\8e04c28b44\hook.dependencies_hash_file.json`)
- **Size**: 425.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### input.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\8e04c28b44\input.json`)
- **Size**: 756.00 B
- **Records**: 3
- **Columns**: 7
- **Missing %**: 28.57%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'assets': 'nan', 'config': "['code_assets/code']", 'out_dir_shared': 'C:\\Users\\mh978\\Downloads\\mobile computing project\\flutter_valorai\\.dart_tool\\hooks_runner\\shared\\objective_c\\build\\', ...`

### output.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\8e04c28b44\output.json`)
- **Size**: 95.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### dependencies.dependencies_hash_file.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\e49245e68d\dependencies.dependencies_hash_file.json`)
- **Size**: 400.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### hook.dependencies_hash_file.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\e49245e68d\hook.dependencies_hash_file.json`)
- **Size**: 425.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### input.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\e49245e68d\input.json`)
- **Size**: 1.26 KB
- **Records**: 3
- **Columns**: 7
- **Missing %**: 28.57%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'assets': 'nan', 'config': "['code_assets/code']", 'out_dir_shared': 'C:\\Users\\mh978\\Downloads\\mobile computing project\\flutter_valorai\\.dart_tool\\hooks_runner\\shared\\objective_c\\build\\', ...`

### output.json (`flutter_valorai\.dart_tool\hooks_runner\objective_c\e49245e68d\output.json`)
- **Size**: 95.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### google-services.json (`flutter_valorai\android\app\google-services.json`)
- **Size**: 1005.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### last_build_run.json (`flutter_valorai\build\last_build_run.json`)
- **Size**: 27.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'0': '--track-widget-creation'}...`

### android_gradle_build.json (`flutter_valorai\build\.cxx\debug\174f2y3d\arm64-v8a\android_gradle_build.json`)
- **Size**: 1.12 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build_mini.json (`flutter_valorai\build\.cxx\debug\174f2y3d\arm64-v8a\android_gradle_build_mini.json`)
- **Size**: 727.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### prefab_config.json (`flutter_valorai\build\.cxx\debug\174f2y3d\arm64-v8a\prefab_config.json`)
- **Size**: 40.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cache-v2-1b88fe7cee18ea25c929.json (`flutter_valorai\build\.cxx\debug\174f2y3d\arm64-v8a\.cmake\api\v1\reply\cache-v2-1b88fe7cee18ea25c929.json`)
- **Size**: 28.38 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cmakeFiles-v1-799c6986d23df26ad8a2.json (`flutter_valorai\build\.cxx\debug\174f2y3d\arm64-v8a\.cmake\api\v1\reply\cmakeFiles-v1-799c6986d23df26ad8a2.json`)
- **Size**: 29.43 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### directory-.-debug-d0094a50bb2071803777.json (`flutter_valorai\build\.cxx\debug\174f2y3d\arm64-v8a\.cmake\api\v1\reply\directory-.-debug-d0094a50bb2071803777.json`)
- **Size**: 168.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### index-2026-06-03T06-56-47-0686.json (`flutter_valorai\build\.cxx\debug\174f2y3d\arm64-v8a\.cmake\api\v1\reply\index-2026-06-03T06-56-47-0686.json`)
- **Size**: 1.71 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build.json (`flutter_valorai\build\.cxx\debug\174f2y3d\armeabi-v7a\android_gradle_build.json`)
- **Size**: 1.12 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build_mini.json (`flutter_valorai\build\.cxx\debug\174f2y3d\armeabi-v7a\android_gradle_build_mini.json`)
- **Size**: 731.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### prefab_config.json (`flutter_valorai\build\.cxx\debug\174f2y3d\armeabi-v7a\prefab_config.json`)
- **Size**: 40.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cache-v2-8d47496c8551736ca113.json (`flutter_valorai\build\.cxx\debug\174f2y3d\armeabi-v7a\.cmake\api\v1\reply\cache-v2-8d47496c8551736ca113.json`)
- **Size**: 28.40 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cmakeFiles-v1-a88f083285687d170931.json (`flutter_valorai\build\.cxx\debug\174f2y3d\armeabi-v7a\.cmake\api\v1\reply\cmakeFiles-v1-a88f083285687d170931.json`)
- **Size**: 29.45 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### directory-.-debug-d0094a50bb2071803777.json (`flutter_valorai\build\.cxx\debug\174f2y3d\armeabi-v7a\.cmake\api\v1\reply\directory-.-debug-d0094a50bb2071803777.json`)
- **Size**: 168.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### index-2026-06-03T06-56-58-0859.json (`flutter_valorai\build\.cxx\debug\174f2y3d\armeabi-v7a\.cmake\api\v1\reply\index-2026-06-03T06-56-58-0859.json`)
- **Size**: 1.71 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build.json (`flutter_valorai\build\.cxx\debug\174f2y3d\x86_64\android_gradle_build.json`)
- **Size**: 1.12 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build_mini.json (`flutter_valorai\build\.cxx\debug\174f2y3d\x86_64\android_gradle_build_mini.json`)
- **Size**: 721.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### prefab_config.json (`flutter_valorai\build\.cxx\debug\174f2y3d\x86_64\prefab_config.json`)
- **Size**: 40.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cache-v2-29ba991fbd559505e08d.json (`flutter_valorai\build\.cxx\debug\174f2y3d\x86_64\.cmake\api\v1\reply\cache-v2-29ba991fbd559505e08d.json`)
- **Size**: 28.37 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cmakeFiles-v1-1aa30eefe01c00ebfd95.json (`flutter_valorai\build\.cxx\debug\174f2y3d\x86_64\.cmake\api\v1\reply\cmakeFiles-v1-1aa30eefe01c00ebfd95.json`)
- **Size**: 29.42 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### directory-.-debug-d0094a50bb2071803777.json (`flutter_valorai\build\.cxx\debug\174f2y3d\x86_64\.cmake\api\v1\reply\directory-.-debug-d0094a50bb2071803777.json`)
- **Size**: 168.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### index-2026-06-03T06-57-04-0623.json (`flutter_valorai\build\.cxx\debug\174f2y3d\x86_64\.cmake\api\v1\reply\index-2026-06-03T06-57-04-0623.json`)
- **Size**: 1.71 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\arm64-v8a\android_gradle_build.json`)
- **Size**: 1.12 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build_mini.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\arm64-v8a\android_gradle_build_mini.json`)
- **Size**: 731.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### prefab_config.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\arm64-v8a\prefab_config.json`)
- **Size**: 40.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cache-v2-9e4d477c670fed8ea4ff.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\arm64-v8a\.cmake\api\v1\reply\cache-v2-9e4d477c670fed8ea4ff.json`)
- **Size**: 28.39 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cmakeFiles-v1-78ce8311af5e1d7a2860.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\arm64-v8a\.cmake\api\v1\reply\cmakeFiles-v1-78ce8311af5e1d7a2860.json`)
- **Size**: 29.45 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### directory-.-release-d0094a50bb2071803777.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\arm64-v8a\.cmake\api\v1\reply\directory-.-release-d0094a50bb2071803777.json`)
- **Size**: 168.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### index-2026-06-03T05-23-14-0820.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\arm64-v8a\.cmake\api\v1\reply\index-2026-06-03T05-23-14-0820.json`)
- **Size**: 1.71 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\armeabi-v7a\android_gradle_build.json`)
- **Size**: 1.13 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build_mini.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\armeabi-v7a\android_gradle_build_mini.json`)
- **Size**: 735.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### prefab_config.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\armeabi-v7a\prefab_config.json`)
- **Size**: 40.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cache-v2-939db4a0c9f040634363.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\armeabi-v7a\.cmake\api\v1\reply\cache-v2-939db4a0c9f040634363.json`)
- **Size**: 28.41 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cmakeFiles-v1-fa03bc654d95cc55fb7c.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\armeabi-v7a\.cmake\api\v1\reply\cmakeFiles-v1-fa03bc654d95cc55fb7c.json`)
- **Size**: 29.46 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### directory-.-release-d0094a50bb2071803777.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\armeabi-v7a\.cmake\api\v1\reply\directory-.-release-d0094a50bb2071803777.json`)
- **Size**: 168.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### index-2026-06-03T05-23-17-0531.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\armeabi-v7a\.cmake\api\v1\reply\index-2026-06-03T05-23-17-0531.json`)
- **Size**: 1.71 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\x86_64\android_gradle_build.json`)
- **Size**: 1.12 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### android_gradle_build_mini.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\x86_64\android_gradle_build_mini.json`)
- **Size**: 725.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### prefab_config.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\x86_64\prefab_config.json`)
- **Size**: 40.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cache-v2-8166fc561aea61041bf7.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\x86_64\.cmake\api\v1\reply\cache-v2-8166fc561aea61041bf7.json`)
- **Size**: 28.38 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### cmakeFiles-v1-bec8c0e3ef41656cf8ce.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\x86_64\.cmake\api\v1\reply\cmakeFiles-v1-bec8c0e3ef41656cf8ce.json`)
- **Size**: 29.43 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### directory-.-release-d0094a50bb2071803777.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\x86_64\.cmake\api\v1\reply\directory-.-release-d0094a50bb2071803777.json`)
- **Size**: 168.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### index-2026-06-03T05-23-19-0769.json (`flutter_valorai\build\.cxx\release\2i3e3f5s\x86_64\.cmake\api\v1\reply\index-2026-06-03T05-23-19-0769.json`)
- **Size**: 1.71 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### deeplink.json (`flutter_valorai\build\app\deeplink.json`)
- **Size**: 445.00 B
- **Records**: 2
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'applicationId': 'com.example.flutter_valorai', 'deeplinkingFlagEnabled': 'False', 'deeplinks': "{'scheme': 'genericidp', 'host': 'firebase.auth', 'path': '/', 'intentFilterCheck': {'hasAutoVerify': ...`

### annotationProcessors.json (`flutter_valorai\build\app\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\app\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### FontManifest.json (`flutter_valorai\build\app\intermediates\assets\debug\mergeDebugAssets\flutter_assets\FontManifest.json`)
- **Size**: 208.00 B
- **Records**: 2
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'family': 'MaterialIcons', 'fonts': "[{'asset': 'fonts/MaterialIcons-Regular.otf'}]"}...`

### NativeAssetsManifest.json (`flutter_valorai\build\app\intermediates\assets\debug\mergeDebugAssets\flutter_assets\NativeAssetsManifest.json`)
- **Size**: 45.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### FontManifest.json (`flutter_valorai\build\app\intermediates\assets\release\mergeReleaseAssets\flutter_assets\FontManifest.json`)
- **Size**: 208.00 B
- **Records**: 2
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'family': 'MaterialIcons', 'fonts': "[{'asset': 'fonts/MaterialIcons-Regular.otf'}]"}...`

### NativeAssetsManifest.json (`flutter_valorai\build\app\intermediates\assets\release\mergeReleaseAssets\flutter_assets\NativeAssetsManifest.json`)
- **Size**: 45.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\compatible_screen_manifest\debug\createDebugCompatibleScreenManifests\output-metadata.json`)
- **Size**: 203.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\compatible_screen_manifest\release\createReleaseCompatibleScreenManifests\output-metadata.json`)
- **Size**: 205.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### metadata_generation_record.json (`flutter_valorai\build\app\intermediates\cxx\debug\174f2y3d\logs\arm64-v8a\metadata_generation_record.json`)
- **Size**: 1.32 KB
- **Records**: 3
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 24 min SDK version: arm64-v8a', 'file_': 'C:\\Users\\mh978\\Downloads\\flutter\\packages\\flutter_tools\\gradle\\src\\main\\script...`

### metadata_generation_record.json (`flutter_valorai\build\app\intermediates\cxx\debug\174f2y3d\logs\armeabi-v7a\metadata_generation_record.json`)
- **Size**: 1.33 KB
- **Records**: 3
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 24 min SDK version: armeabi-v7a', 'file_': 'C:\\Users\\mh978\\Downloads\\flutter\\packages\\flutter_tools\\gradle\\src\\main\\scri...`

### metadata_generation_record.json (`flutter_valorai\build\app\intermediates\cxx\debug\174f2y3d\logs\x86_64\metadata_generation_record.json`)
- **Size**: 1.31 KB
- **Records**: 3
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 24 min SDK version: x86_64', 'file_': 'C:\\Users\\mh978\\Downloads\\flutter\\packages\\flutter_tools\\gradle\\src\\main\\scripts\\...`

### metadata_generation_record.json (`flutter_valorai\build\app\intermediates\cxx\release\2i3e3f5s\logs\arm64-v8a\metadata_generation_record.json`)
- **Size**: 8.10 KB
- **Records**: 11
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 24 min SDK version: arm64-v8a', 'file_': 'C:\\Users\\mh978\\Downloads\\flutter\\packages\\flutter_tools\\gradle\\src\\main\\script...`

### metadata_generation_record.json (`flutter_valorai\build\app\intermediates\cxx\release\2i3e3f5s\logs\armeabi-v7a\metadata_generation_record.json`)
- **Size**: 8.15 KB
- **Records**: 11
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 24 min SDK version: armeabi-v7a', 'file_': 'C:\\Users\\mh978\\Downloads\\flutter\\packages\\flutter_tools\\gradle\\src\\main\\scri...`

### metadata_generation_record.json (`flutter_valorai\build\app\intermediates\cxx\release\2i3e3f5s\logs\x86_64\metadata_generation_record.json`)
- **Size**: 8.02 KB
- **Records**: 11
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 24 min SDK version: x86_64', 'file_': 'C:\\Users\\mh978\\Downloads\\flutter\\packages\\flutter_tools\\gradle\\src\\main\\scripts\\...`

### FontManifest.json (`flutter_valorai\build\app\intermediates\flutter\debug\flutter_assets\FontManifest.json`)
- **Size**: 208.00 B
- **Records**: 2
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'family': 'MaterialIcons', 'fonts': "[{'asset': 'fonts/MaterialIcons-Regular.otf'}]"}...`

### NativeAssetsManifest.json (`flutter_valorai\build\app\intermediates\flutter\debug\flutter_assets\NativeAssetsManifest.json`)
- **Size**: 45.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### FontManifest.json (`flutter_valorai\build\app\intermediates\flutter\release\flutter_assets\FontManifest.json`)
- **Size**: 208.00 B
- **Records**: 2
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'family': 'MaterialIcons', 'fonts': "[{'asset': 'fonts/MaterialIcons-Regular.otf'}]"}...`

### NativeAssetsManifest.json (`flutter_valorai\build\app\intermediates\flutter\release\flutter_assets\NativeAssetsManifest.json`)
- **Size**: 45.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### kotlin-tooling-metadata.json (`flutter_valorai\build\app\intermediates\java_res\release\processReleaseJavaRes\out\kotlin-tooling-metadata.json`)
- **Size**: 625.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\linked_resources_binary_format\debug\processDebugResources\output-metadata.json`)
- **Size**: 433.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\linked_resources_proto_format\release\processReleaseResources\output-metadata.json`)
- **Size**: 435.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\merged_manifests\debug\processDebugManifest\output-metadata.json`)
- **Size**: 398.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\merged_manifests\release\processReleaseManifest\output-metadata.json`)
- **Size**: 400.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### mergeDebugResources.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\mergeDebugResources.json`)
- **Size**: 722.30 KB
- **Records**: 107
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-debug-46:/values-zu_values-zu.arsc.flat', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd015edb54...`

### values-af.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-af.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-am.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-am.json`)
- **Size**: 7.68 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c521...`

### values-ar.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ar.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-as.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-as.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71c1...`

### values-az.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-az.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95bd6...`

### values-b+sr+Latn.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 7.80 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-be.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-be.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-bg.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-bg.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-bn.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-bn.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-bs.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-bs.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f847a...`

### values-ca.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ca.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-cs.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-cs.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-da.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-da.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c521...`

### values-de.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-de.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71c1...`

### values-el.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-el.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f847a...`

### values-en-rAU.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 5.65 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-en-rCA.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 5.65 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-en-rGB.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 7.75 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-en-rIN.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 5.65 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-en-rXC.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 5.75 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-es-rUS.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 7.77 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-es.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-es.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-et.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-et.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-eu.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-eu.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f847a...`

### values-fa.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-fa.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c521...`

### values-fi.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-fi.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-fr-rCA.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 7.77 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-fr.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-fr.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-gl.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-gl.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-gu.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-gu.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71c1...`

### values-h720dp-v13.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-h720dp-v13.json`)
- **Size**: 709.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-h720dp-v13/values-h720dp-v13.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-hdpi-v4.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-hdpi-v4.json`)
- **Size**: 738.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-hdpi-v4/values-hdpi-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-hi.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-hi.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95bd6...`

### values-hr.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-hr.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c521...`

### values-hu.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-hu.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-hy.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-hy.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-in.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-in.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-is.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-is.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-it.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-it.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c521...`

### values-iw.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-iw.json`)
- **Size**: 7.69 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f847a...`

### values-ja.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ja.json`)
- **Size**: 7.68 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71c1...`

### values-ka.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ka.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f847a...`

### values-kk.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-kk.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-km.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-km.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-kn.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-kn.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-ko.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ko.json`)
- **Size**: 7.67 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c521...`

### values-ky.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ky.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71c1...`

### values-land.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-land.json`)
- **Size**: 715.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-land/values-land.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-large-v4.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-large-v4.json`)
- **Size**: 824.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-large-v4/values-large-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-ldltr-v21.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ldltr-v21.json`)
- **Size**: 706.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ldltr-v21/values-ldltr-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-lo.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-lo.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-lt.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-lt.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-lv.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-lv.json`)
- **Size**: 7.73 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95bd6...`

### values-mk.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-mk.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-ml.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ml.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95bd6...`

### values-mn.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-mn.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c521...`

### values-mr.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-mr.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f847a...`

### values-ms.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ms.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95bd6...`

### values-my.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-my.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f847a...`

### values-nb.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-nb.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-ne.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ne.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-night-v8.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-night-v8.json`)
- **Size**: 2.01 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-night-v8/values-night-v8.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\Downloads\\\\mobile computing projec...`

### values-nl.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-nl.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c521...`

### values-or.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-or.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f847a...`

### values-pa.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-pa.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-pl.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-pl.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71c1...`

### values-port.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-port.json`)
- **Size**: 685.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-port/values-port.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-pt-rBR.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 7.77 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-pt-rPT.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 7.76 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-pt.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-pt.json`)
- **Size**: 5.62 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-ro.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ro.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71c1...`

### values-ru.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ru.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f847a...`

### values-si.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-si.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-sk.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-sk.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-sl.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-sl.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-sq.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-sq.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-sr.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-sr.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-sv.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-sv.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-sw.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-sw.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-sw600dp-v13.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-sw600dp-v13.json`)
- **Size**: 818.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-sw600dp-v13/values-sw600dp-v13.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\t...`

### values-ta.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ta.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-te.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-te.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-th.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-th.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c521...`

### values-tl.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-tl.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-tr.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-tr.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-uk.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-uk.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values-ur.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-ur.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-uz.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-uz.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e92a...`

### values-v16.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-v16.json`)
- **Size**: 722.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-v16/values-v16.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-v17.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-v17.json`)
- **Size**: 1.02 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-v17/values-v17.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-v18.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-v18.json`)
- **Size**: 680.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-v18/values-v18.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-v21.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-v21.json`)
- **Size**: 7.08 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-v22.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-v22.json`)
- **Size**: 774.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-v22/values-v22.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-v23.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-v23.json`)
- **Size**: 988.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-v23/values-v23.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-v24.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-v24.json`)
- **Size**: 698.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-v24/values-v24.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-v25.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-v25.json`)
- **Size**: 773.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-v25/values-v25.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-v26.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-v26.json`)
- **Size**: 812.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-v26/values-v26.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-v28.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-v28.json`)
- **Size**: 774.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-v28/values-v28.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-vi.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-vi.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d0b...`

### values-watch-v20.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-watch-v20.json`)
- **Size**: 2.08 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-watch-v20/values-watch-v20.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-watch-v21.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-watch-v21.json`)
- **Size**: 782.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-watch-v21/values-watch-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-xlarge-v4.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-xlarge-v4.json`)
- **Size**: 780.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-xlarge-v4/values-xlarge-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-zh-rCN.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-zh-rHK.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-zh-rTW.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-zu.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values-zu.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03cdd...`

### values.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\multi-v2\values.json`)
- **Size**: 55.16 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeDebugResources-44:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\2601acb2214...`

### mergeDebugResources.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\debug\mergeDebugResources\out\single\mergeDebugResources.json`)
- **Size**: 1.19 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.example.flutter_valorai.app-debug-46:/mipmap-xxxhdpi_ic_launcher.png.flat', 'source': 'com.example.flutter_valorai.app-main-40:/mipmap-xxxhdpi/ic_launcher.png'}...`

### mergeReleaseResources.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\mergeReleaseResources.json`)
- **Size**: 722.51 KB
- **Records**: 107
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-release-47:/values-ru_values-ru.arsc.flat', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f847a352b88...`

### values-af.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-am.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 7.68 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c5...`

### values-ar.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-as.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71...`

### values-az.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95b...`

### values-b+sr+Latn.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 7.81 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-be.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-bg.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-bn.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-bs.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f84...`

### values-ca.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-cs.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-da.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c5...`

### values-de.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71...`

### values-el.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f84...`

### values-en-rAU.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 5.65 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-en-rCA.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 5.65 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-en-rGB.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 7.75 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-en-rIN.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 5.65 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-en-rXC.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 5.75 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-es-rUS.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 7.77 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-es.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-et.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-eu.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f84...`

### values-fa.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c5...`

### values-fi.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-fr-rCA.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 7.78 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-fr.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-gl.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-gu.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71...`

### values-h720dp-v13.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-h720dp-v13.json`)
- **Size**: 711.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-h720dp-v13/values-h720dp-v13.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\t...`

### values-hdpi-v4.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hdpi-v4.json`)
- **Size**: 740.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-hdpi-v4/values-hdpi-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-hi.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95b...`

### values-hr.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c5...`

### values-hu.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-hy.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-in.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-is.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-it.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c5...`

### values-iw.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f84...`

### values-ja.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 7.68 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71...`

### values-ka.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f84...`

### values-kk.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-km.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-kn.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-ko.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 7.67 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c5...`

### values-ky.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71...`

### values-land.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-land.json`)
- **Size**: 717.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-land/values-land.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\...`

### values-large-v4.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-large-v4.json`)
- **Size**: 826.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-large-v4/values-large-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-ldltr-v21.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ldltr-v21.json`)
- **Size**: 708.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ldltr-v21/values-ldltr-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-lo.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-lt.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-lv.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 7.73 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95b...`

### values-mk.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-ml.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95b...`

### values-mn.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c5...`

### values-mr.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f84...`

### values-ms.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95b...`

### values-my.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f84...`

### values-nb.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-ne.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-night-v8.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-night-v8.json`)
- **Size**: 2.02 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-night-v8/values-night-v8.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\Downloads\\\\mobile computing proj...`

### values-nl.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c5...`

### values-or.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 7.73 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f84...`

### values-pa.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-pl.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71...`

### values-port.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-port.json`)
- **Size**: 687.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-port/values-port.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\...`

### values-pt-rBR.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 7.77 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-pt-rPT.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 7.77 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-pt.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 5.62 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-ro.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\b71...`

### values-ru.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f84...`

### values-si.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-sk.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-sl.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-sq.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-sr.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-sv.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-sw.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-sw600dp-v13.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw600dp-v13.json`)
- **Size**: 820.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-sw600dp-v13/values-sw600dp-v13.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\...`

### values-ta.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-te.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-th.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 7.70 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\3c5...`

### values-tl.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-tr.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-uk.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values-ur.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 7.72 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-uz.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8e9...`

### values-v16.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v16.json`)
- **Size**: 724.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-v16/values-v16.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-v17.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v17.json`)
- **Size**: 1.02 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-v17/values-v17.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-v18.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v18.json`)
- **Size**: 682.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-v18/values-v18.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-v21.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 7.08 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-v22.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v22.json`)
- **Size**: 776.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-v22/values-v22.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-v23.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v23.json`)
- **Size**: 990.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-v23/values-v23.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-v24.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v24.json`)
- **Size**: 700.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-v24/values-v24.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-v25.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v25.json`)
- **Size**: 775.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-v25/values-v25.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-v26.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v26.json`)
- **Size**: 814.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-v26/values-v26.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-v28.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v28.json`)
- **Size**: 776.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-v28/values-v28.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8...`

### values-vi.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\93d...`

### values-watch-v20.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-watch-v20.json`)
- **Size**: 2.08 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-watch-v20/values-watch-v20.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-watch-v21.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-watch-v21.json`)
- **Size**: 784.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-watch-v21/values-watch-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-xlarge-v4.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-xlarge-v4.json`)
- **Size**: 782.00 B
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-xlarge-v4/values-xlarge-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-zh-rCN.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-zh-rHK.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-zh-rTW.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-zu.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 7.71 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\03c...`

### values.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 55.16 KB
- **Records**: 1
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.example.flutter_valorai.app-mergeReleaseResources-44:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\2601acb22...`

### mergeReleaseResources.json (`flutter_valorai\build\app\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\mergeReleaseResources.json`)
- **Size**: 103.73 KB
- **Records**: 419
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.example.flutter_valorai.app-release-47:/drawable-mdpi-v4_abc_tab_indicator_mtrl_alpha.9.png.flat', 'source': 'com.example.flutter_valorai.app-appcompat-1.7.1-17:/drawable-mdpi-v4/abc_t...`

### navigation.json (`flutter_valorai\build\app\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\app\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\optimized_processed_res\release\optimizeReleaseResources\output-metadata.json`)
- **Size**: 418.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\packaged_manifests\debug\processDebugManifestForPackage\output-metadata.json`)
- **Size**: 400.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\packaged_manifests\release\processReleaseManifestForPackage\output-metadata.json`)
- **Size**: 402.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\shrunk_resources_binary_format\release\convertShrunkResourcesToBinaryRelease\output-metadata.json`)
- **Size**: 437.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\intermediates\shrunk_resources_proto_format\release\minifyReleaseWithR8\output-metadata.json`)
- **Size**: 435.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### signing-config-versions.json (`flutter_valorai\build\app\intermediates\signing_config_versions\debug\writeDebugSigningConfigVersions\signing-config-versions.json`)
- **Size**: 96.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### signing-config-versions.json (`flutter_valorai\build\app\intermediates\signing_config_versions\release\writeReleaseSigningConfigVersions\signing-config-versions.json`)
- **Size**: 96.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### kotlin-tooling-metadata.json (`flutter_valorai\build\app\kotlinToolingMetadata\kotlin-tooling-metadata.json`)
- **Size**: 625.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\outputs\apk\debug\output-metadata.json`)
- **Size**: 411.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\app\outputs\apk\release\output-metadata.json`)
- **Size**: 717.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\cloud_firestore\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 368.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\cloud_firestore\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 370.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\cloud_firestore\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\cloud_firestore\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### values-af.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-am.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-ar.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-as.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-az.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-b+sr+Latn.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 6.56 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-be.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-bg.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-bn.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-bs.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-ca.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-cs.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-da.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-de.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-el.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-en-rAU.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cache...`

### values-en-rCA.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\t...`

### values-en-rGB.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 6.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cache...`

### values-en-rIN.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\t...`

### values-en-rXC.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 1.59 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\t...`

### values-es-rUS.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 6.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\t...`

### values-es.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-et.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-eu.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-fa.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-fi.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-fr-rCA.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 6.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cache...`

### values-fr.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-gl.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-gu.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-hi.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-hr.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-hu.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-hy.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-in.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-is.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-it.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-iw.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-ja.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-ka.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-kk.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-km.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-kn.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-ko.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 6.45 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-ky.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-lo.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-lt.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-lv.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-mk.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-ml.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-mn.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-mr.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-ms.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-my.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-nb.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-ne.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-nl.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-or.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-pa.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-pl.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-pt-rBR.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 6.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\t...`

### values-pt-rPT.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 6.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cache...`

### values-pt.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-ro.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-ru.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-si.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-sk.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-sl.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-sq.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-sr.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-sv.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-sw.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-ta.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-te.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-th.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-tl.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-tr.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-uk.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-ur.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-mergeReleaseResources-31:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.1...`

### values-uz.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-v21.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 1.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-vi.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-zh-rCN.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\t...`

### values-zh-rHK.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 6.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\t...`

### values-zh-rTW.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\t...`

### values-zu.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 6.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 28.83 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\2...`

### anim-v21.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 284.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-fragment-1...`

### animator.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.51 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/animator/fragment_close_exit.xml', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-fragment-1.7.1-1:/anim...`

### color.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\color.json`)
- **Size**: 876.00 B
- **Records**: 3
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/color/common_google_signin_btn_tint.xml', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-play-services-b...`

### drawable-anydpi-v21.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v21.json`)
- **Size**: 1.62 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/drawable-anydpi-v21/ic_call_answer_low.xml', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-core-1.13.1-...`

### drawable-hdpi-v4.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 5.58 KB
- **Records**: 19
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/drawable-hdpi-v4/common_full_open_on_phone.png', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-play-ser...`

### drawable-ldpi-v4.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldpi-v4.json`)
- **Size**: 1.59 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/drawable-ldpi-v4/ic_call_answer_low.png', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-core-1.13.1-23:...`

### drawable-mdpi-v4.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 4.99 KB
- **Records**: 17
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/drawable-mdpi-v4/ic_call_answer.png', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-core-1.13.1-23:/dra...`

### drawable-v21.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 288.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/drawable-v21/notification_action_background.xml', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-core-1....`

### drawable-xhdpi-v4.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 5.32 KB
- **Records**: 18
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/drawable-xhdpi-v4/googleg_standard_color_18.png', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-play-se...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 3.61 KB
- **Records**: 12
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/drawable-xxhdpi-v4/ic_call_decline.png', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-core-1.13.1-23:/...`

### drawable-xxxhdpi-v4.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v4.json`)
- **Size**: 1.62 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/drawable-xxxhdpi-v4/ic_call_answer_video_low.png', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-core-1...`

### drawable.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 5.26 KB
- **Records**: 18
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/drawable/common_google_signin_btn_icon_light_normal.xml', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore...`

### layout-v21.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 1.09 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/layout-v21/notification_action_tombstone.xml', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-core-1.13....`

### layout.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 1.33 KB
- **Records**: 5
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/layout/custom_dialog.xml', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-core-1.13.1-23:/layout/custom_...`

### raw.json (`flutter_valorai\build\cloud_firestore\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\raw.json`)
- **Size**: 261.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.firestore.cloud_firestore-release-33:/raw/firebase_common_keep.xml', 'source': 'io.flutter.plugins.firebase.firestore.cloud_firestore-firebase-common-22.0.1-18:...`

### navigation.json (`flutter_valorai\build\cloud_firestore\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\cloud_firestore\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\firebase_auth\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 363.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\firebase_auth\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 365.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\firebase_auth\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\firebase_auth\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### values-af.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-am.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 9.15 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ar.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-as.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-az.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-b+sr+Latn.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 9.32 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-be.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\36...`

### values-bg.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-bn.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-bs.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-ca.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-cs.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-da.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-de.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-el.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-en-rAU.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 5.05 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-en-rCA.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 5.04 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-en-rGB.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 9.25 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-en-rIN.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 5.05 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-en-rXC.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 5.10 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-es-rUS.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 9.27 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-es.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95...`

### values-et.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-eu.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f8...`

### values-fa.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-fi.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-fr-rCA.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 9.28 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-fr.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-gl.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-gu.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-hi.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\36...`

### values-hr.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95...`

### values-hu.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-hy.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\36...`

### values-in.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f8...`

### values-is.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-it.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-iw.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 9.17 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ja.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 9.15 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ka.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f8...`

### values-kk.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95...`

### values-km.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95...`

### values-kn.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ko.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 9.14 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95...`

### values-ky.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-lo.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 9.17 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-lt.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-lv.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-mk.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ml.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 9.21 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-mn.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-mr.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ms.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\36...`

### values-my.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-nb.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ne.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-nl.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\36...`

### values-or.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-pa.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-pl.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\36...`

### values-pt-rBR.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 9.26 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-pt-rPT.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 9.26 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-pt.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 4.99 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ro.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\36...`

### values-ru.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-si.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-sk.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\95...`

### values-sl.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-sq.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f8...`

### values-sr.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-sv.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\f8...`

### values-sw.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ta.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-te.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-th.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-tl.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-tr.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 9.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-uk.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ur.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-uz.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 9.20 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\1e...`

### values-v21.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 4.38 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\...`

### values-vi.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-watch-v20.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-watch-v20.json`)
- **Size**: 2.32 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-watch-v20/values-watch-v20.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches...`

### values-zh-rCN.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 9.22 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-zh-rHK.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 9.22 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-zh-rTW.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 9.21 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-zu.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 9.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 35.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.auth.firebase_auth-mergeReleaseResources-36:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### anim-v21.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 270.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-fragment-1.7.1-1:/anim-v...`

### animator.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.43 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/animator/fragment_open_enter.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-fragment-1.7.1-1:/animator/fragment_...`

### color.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\color.json`)
- **Size**: 834.00 B
- **Records**: 3
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/color/common_google_signin_btn_text_light.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-play-services-base-18.0...`

### drawable-anydpi-v21.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v21.json`)
- **Size**: 2.05 KB
- **Records**: 8
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable-anydpi-v21/ic_call_answer.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-core-1.13.1-28:/drawable-anydp...`

### drawable-anydpi-v24.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v24.json`)
- **Size**: 258.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable-anydpi-v24/ic_passkey.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-credentials-1.2.0-rc01-6:/drawable...`

### drawable-hdpi-v4.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 6.07 KB
- **Records**: 22
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable-hdpi-v4/ic_call_answer_low.png', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-core-1.13.1-28:/drawable-hdpi...`

### drawable-ldpi-v4.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldpi-v4.json`)
- **Size**: 2.25 KB
- **Records**: 9
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable-ldpi-v4/ic_call_answer_low.png', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-core-1.13.1-28:/drawable-ldpi...`

### drawable-mdpi-v4.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 5.51 KB
- **Records**: 20
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable-mdpi-v4/googleg_standard_color_18.png', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-play-services-base-18....`

### drawable-v21.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 274.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable-v21/notification_action_background.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-core-1.13.1-28:/drawa...`

### drawable-watch-v20.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-watch-v20.json`)
- **Size**: 958.00 B
- **Records**: 3
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable-watch-v20/common_google_signin_btn_text_dark_normal.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-play...`

### drawable-xhdpi-v4.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 5.82 KB
- **Records**: 21
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable-xhdpi-v4/ic_other_sign_in.png', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-credentials-1.2.0-rc01-6:/draw...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 4.21 KB
- **Records**: 15
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable-xxhdpi-v4/googleg_disabled_color_18.png', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-play-services-base-1...`

### drawable-xxxhdpi-v4.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v4.json`)
- **Size**: 2.30 KB
- **Records**: 9
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable-xxxhdpi-v4/ic_call_answer_video_low.png', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-core-1.13.1-28:/draw...`

### drawable.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 5.01 KB
- **Records**: 18
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/drawable/common_google_signin_btn_icon_dark.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-play-services-base-18...`

### layout-v21.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 1.03 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/layout-v21/notification_template_custom_big.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-core-1.13.1-28:/layou...`

### layout.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 1.78 KB
- **Records**: 7
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/layout/browser_actions_context_menu_row.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-browser-1.4.0-17:/layout/...`

### raw.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\raw.json`)
- **Size**: 247.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/raw/firebase_common_keep.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-firebase-common-22.0.1-23:/raw/firebase_...`

### xml.json (`flutter_valorai\build\firebase_auth\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\xml.json`)
- **Size**: 240.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.auth.firebase_auth-release-38:/xml/image_share_filepaths.xml', 'source': 'io.flutter.plugins.firebase.auth.firebase_auth-browser-1.4.0-17:/xml/image_share_filep...`

### navigation.json (`flutter_valorai\build\firebase_auth\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\firebase_auth\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\firebase_core\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 363.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\firebase_core\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 365.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\firebase_core\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\firebase_core\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### values-af.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-am.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 3.79 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-ar.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-as.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-az.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-b+sr+Latn.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 3.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-be.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-bg.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-bn.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-bs.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ca.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-cs.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-da.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-de.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-el.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-en-rAU.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 1.56 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-en-rCA.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 1.56 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-en-rGB.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 3.84 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-en-rIN.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 1.56 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-en-rXC.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-es-rUS.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 3.84 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-es.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-et.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-eu.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-fa.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-fi.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-fr-rCA.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 3.84 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-fr.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-gl.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-gu.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-hi.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-hr.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-hu.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-hy.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-in.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-is.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-it.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-iw.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 3.79 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-ja.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 3.79 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ka.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-kk.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-km.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-kn.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ko.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 3.78 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ky.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-lo.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 3.79 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-lt.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-lv.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-mk.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-ml.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-mn.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-mr.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ms.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-my.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-nb.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-ne.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-nl.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-or.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-pa.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-pl.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-pt-rBR.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 3.84 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-pt-rPT.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 3.84 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-pt.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ro.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ru.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-si.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-sk.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-sl.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-sq.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-sr.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-sv.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-sw.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ta.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-te.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-th.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-tl.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-tr.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-uk.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-ur.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-uz.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 3.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fd...`

### values-v21.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 1.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\...`

### values-vi.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-zh-rCN.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 3.82 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-zh-rHK.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 3.82 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-zh-rTW.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 3.82 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-zu.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 3.80 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 24.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.firebase.core.firebase_core-mergeReleaseResources-30:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### anim-v21.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 270.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'io.flutter.plugins.firebase.core.firebase_core-fragment-1.7.1-1:/anim-v...`

### animator.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.43 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/animator/fragment_open_exit.xml', 'source': 'io.flutter.plugins.firebase.core.firebase_core-fragment-1.7.1-1:/animator/fragment_o...`

### drawable-anydpi-v21.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v21.json`)
- **Size**: 1.54 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/drawable-anydpi-v21/ic_call_decline_low.xml', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/drawable-...`

### drawable-hdpi-v4.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 3.15 KB
- **Records**: 12
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/drawable-hdpi-v4/notification_bg_normal.9.png', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/drawabl...`

### drawable-ldpi-v4.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldpi-v4.json`)
- **Size**: 1.51 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/drawable-ldpi-v4/ic_call_answer_video_low.png', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/drawabl...`

### drawable-mdpi-v4.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 2.87 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/drawable-mdpi-v4/ic_call_decline.png', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/drawable-mdpi-v4...`

### drawable-v21.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 274.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/drawable-v21/notification_action_background.xml', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/drawa...`

### drawable-xhdpi-v4.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 2.89 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/drawable-xhdpi-v4/ic_call_answer_video.png', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/drawable-x...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 1.53 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/drawable-xxhdpi-v4/ic_call_answer_video_low.png', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/drawa...`

### drawable-xxxhdpi-v4.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v4.json`)
- **Size**: 1.54 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/drawable-xxxhdpi-v4/ic_call_decline.png', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/drawable-xxxh...`

### drawable.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 982.00 B
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/drawable/notification_tile_bg.xml', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/drawable/notificati...`

### layout-v21.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 1.03 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/layout-v21/notification_action_tombstone.xml', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/layout-v...`

### layout.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 1.26 KB
- **Records**: 5
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/layout/ime_base_split_test_activity.xml', 'source': 'io.flutter.plugins.firebase.core.firebase_core-core-1.13.1-22:/layout/ime_ba...`

### raw.json (`flutter_valorai\build\firebase_core\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\raw.json`)
- **Size**: 247.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.firebase.core.firebase_core-release-32:/raw/firebase_common_keep.xml', 'source': 'io.flutter.plugins.firebase.core.firebase_core-firebase-common-22.0.1-17:/raw/firebase_...`

### navigation.json (`flutter_valorai\build\firebase_core\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\firebase_core\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 382.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 384.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### values-af.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-am.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-ar.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-as.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-az.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-b+sr+Latn.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 1.59 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-be.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-bg.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-bn.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-bs.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-ca.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-cs.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-da.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-de.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-el.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-en-rAU.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\...`

### values-en-rCA.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\...`

### values-en-rGB.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\...`

### values-en-rIN.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\...`

### values-en-rXC.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 1.59 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-es-rUS.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-es.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-et.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-eu.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-fa.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-fi.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-fr-rCA.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\...`

### values-fr.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-gl.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-gu.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-hi.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-hr.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-hu.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-hy.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-in.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-is.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-it.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-iw.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-ja.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-ka.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-kk.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-km.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-kn.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-ko.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-ky.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-lo.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-lt.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-lv.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-mk.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-ml.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-mn.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-mr.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-ms.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-my.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-nb.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-ne.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-nl.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-or.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-pa.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-pl.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-pt-rBR.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\...`

### values-pt-rPT.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-pt.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-ro.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-ru.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-si.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-sk.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-sl.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-sq.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-sr.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-sv.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-sw.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-ta.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-te.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-th.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-tl.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-tr.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-uk.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-ur.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### values-uz.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-v21.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 1.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transform...`

### values-vi.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-zh-rCN.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 1.56 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-zh-rHK.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 1.56 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\...`

### values-zh-rTW.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 1.56 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-zu.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-mergeReleaseResources-24:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 23.23 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\260...`

### anim-v21.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 280.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-fragment-1.7.1...`

### animator.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.49 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/animator/fragment_open_enter.xml', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-fragment-1.7.1-1:/animator...`

### drawable-anydpi-v21.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v21.json`)
- **Size**: 1.60 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/drawable-anydpi-v21/ic_call_decline.xml', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1-18:/dra...`

### drawable-hdpi-v4.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 3.27 KB
- **Records**: 12
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/drawable-hdpi-v4/ic_call_answer_video.png', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1-18:/d...`

### drawable-ldpi-v4.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldpi-v4.json`)
- **Size**: 1.56 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/drawable-ldpi-v4/ic_call_answer_low.png', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1-18:/dra...`

### drawable-mdpi-v4.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 2.97 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/drawable-mdpi-v4/ic_call_decline_low.png', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1-18:/dr...`

### drawable-v21.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 284.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/drawable-v21/notification_action_background.xml', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1...`

### drawable-xhdpi-v4.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 2.99 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/drawable-xhdpi-v4/notification_bg_normal.9.png', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1-...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 1.59 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/drawable-xxhdpi-v4/ic_call_decline.png', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1-18:/draw...`

### drawable-xxxhdpi-v4.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v4.json`)
- **Size**: 1.60 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/drawable-xxxhdpi-v4/ic_call_answer_video.png', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1-18...`

### drawable.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 1022.00 B
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/drawable/notification_tile_bg.xml', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1-18:/drawable/...`

### layout-v21.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 1.07 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/layout-v21/notification_action_tombstone.xml', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1-18...`

### layout.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 1.31 KB
- **Records**: 5
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.flutter_plugin_android_lifecycle-release-26:/layout/custom_dialog.xml', 'source': 'io.flutter.plugins.flutter_plugin_android_lifecycle-core-1.13.1-18:/layout/custom_dial...`

### navigation.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\flutter_plugin_android_lifecycle\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\flutter_secure_storage\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 365.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\flutter_secure_storage\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 367.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\flutter_secure_storage\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\flutter_secure_storage\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### values-af.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-am.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ar.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-as.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-az.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-b+sr+Latn.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 1.61 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-be.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-bg.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-bn.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-bs.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ca.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-cs.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-da.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-de.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-el.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-en-rAU.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-en-rCA.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-en-rGB.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-en-rIN.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-en-rXC.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 1.60 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-es-rUS.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-es.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-et.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-eu.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-fa.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-fi.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-fr-rCA.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-fr.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-gl.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-gu.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-hi.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-hr.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-hu.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-hy.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-in.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-is.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-it.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-iw.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ja.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-ka.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-kk.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-km.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-kn.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-ko.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-ky.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-lo.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-lt.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-lv.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-mk.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ml.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-mn.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-mr.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ms.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-my.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-nb.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-ne.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-nl.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-or.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-pa.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-pl.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-pt-rBR.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-pt-rPT.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-pt.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ro.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ru.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-si.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-sk.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-sl.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-sq.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-sr.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-sv.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-sw.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ta.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-te.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-th.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-tl.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-tr.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-uk.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ur.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-uz.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-v21.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 1.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\...`

### values-vi.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-zh-rCN.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-zh-rHK.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-zh-rTW.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-mergeReleaseResources-24:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-zu.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 23.24 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\...`

### anim-v21.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 292.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-fr...`

### animator.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.56 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/animator/fragment_fade_enter.xml', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-fragment-1.7.1...`

### drawable-anydpi-v21.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v21.json`)
- **Size**: 1.67 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/drawable-anydpi-v21/ic_call_answer_video_low.xml', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storag...`

### drawable-hdpi-v4.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 3.41 KB
- **Records**: 12
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/drawable-hdpi-v4/notification_bg_normal.9.png', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-c...`

### drawable-ldpi-v4.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldpi-v4.json`)
- **Size**: 1.63 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/drawable-ldpi-v4/ic_call_answer.png', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-core-1.13.1...`

### drawable-mdpi-v4.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 3.10 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/drawable-mdpi-v4/notification_bg_low_pressed.9.png', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_stor...`

### drawable-v21.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 296.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/drawable-v21/notification_action_background.xml', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage...`

### drawable-xhdpi-v4.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 3.12 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/drawable-xhdpi-v4/ic_call_decline.png', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-core-1.13...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 1.66 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/drawable-xxhdpi-v4/ic_call_answer_low.png', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-core-...`

### drawable-xxxhdpi-v4.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v4.json`)
- **Size**: 1.67 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/drawable-xxxhdpi-v4/ic_call_decline.png', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-core-1....`

### drawable.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 1.04 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/drawable/notification_bg.xml', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-core-1.13.1-18:/dr...`

### layout-v21.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 1.12 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/layout-v21/notification_action.xml', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-core-1.13.1-...`

### layout.json (`flutter_valorai\build\flutter_secure_storage\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 1.37 KB
- **Records**: 5
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-release-26:/layout/ime_base_split_test_activity.xml', 'source': 'com.it_nomads.fluttersecurestorage.flutter_secure_storage-core-1....`

### navigation.json (`flutter_valorai\build\flutter_secure_storage\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\flutter_secure_storage\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\geolocator_android\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 354.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\geolocator_android\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 356.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\geolocator_android\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\geolocator_android\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### values-af.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-am.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 6.43 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-ar.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-as.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-az.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-b+sr+Latn.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 6.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-be.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-bg.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-bn.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-bs.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-ca.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-cs.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-da.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-de.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8dd7a9...`

### values-el.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8dd7a9...`

### values-en-rAU.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\...`

### values-en-rCA.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\...`

### values-en-rGB.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 6.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\...`

### values-en-rIN.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\...`

### values-en-rXC.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\...`

### values-es-rUS.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 6.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\...`

### values-es.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8dd7a9...`

### values-et.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-eu.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-fa.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 6.45 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-fi.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-fr-rCA.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 6.51 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\...`

### values-fr.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-gl.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-gu.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 6.45 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-hi.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-hr.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-hu.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8dd7a9...`

### values-hy.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-in.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-is.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-it.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-iw.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 6.45 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8dd7a9...`

### values-ja.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 6.43 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-ka.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8dd7a9...`

### values-kk.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-km.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8dd7a9...`

### values-kn.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-ko.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 6.42 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-ky.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-lo.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 6.45 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-lt.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-lv.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-mk.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-ml.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-mn.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-mr.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8dd7a9...`

### values-ms.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-my.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-nb.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-ne.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-nl.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-or.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-pa.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-pl.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 6.45 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-pt-rBR.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 6.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\...`

### values-pt-rPT.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 6.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\...`

### values-pt.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-ro.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-ru.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-si.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-sk.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-sl.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-sq.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-sr.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-sv.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-sw.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8dd7a9...`

### values-ta.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-te.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-th.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\fda1b2...`

### values-tl.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\8dd7a9...`

### values-tr.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-uk.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-ur.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-uz.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-v21.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 1.71 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765...`

### values-vi.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 6.45 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values-zh-rCN.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\...`

### values-zh-rHK.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 6.47 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\...`

### values-zh-rTW.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-mergeReleaseResources-27:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\...`

### values-zu.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 6.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\5765d7...`

### values.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 30.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.baseflow.geolocator.geolocator_android-release-29:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\2601acb22147...`

### anim-v21.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 262.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'com.baseflow.geolocator.geolocator_android-fragment-1.7.1-1:/anim-v21/fragm...`

### animator.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.38 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/animator/fragment_fade_exit.xml', 'source': 'com.baseflow.geolocator.geolocator_android-fragment-1.7.1-1:/animator/fragment_fade_exit...`

### color.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\color.json`)
- **Size**: 810.00 B
- **Records**: 3
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/color/common_google_signin_btn_text_dark.xml', 'source': 'com.baseflow.geolocator.geolocator_android-play-services-base-18.3.0-13:/co...`

### drawable-hdpi-v4.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 3.71 KB
- **Records**: 13
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/drawable-hdpi-v4/common_full_open_on_phone.png', 'source': 'com.baseflow.geolocator.geolocator_android-play-services-base-18.3.0-13:/...`

### drawable-mdpi-v4.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 3.17 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/drawable-mdpi-v4/notification_bg_low_pressed.9.png', 'source': 'com.baseflow.geolocator.geolocator_android-core-1.16.0-11:/drawable-m...`

### drawable-v21.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 266.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/drawable-v21/notification_action_background.xml', 'source': 'com.baseflow.geolocator.geolocator_android-core-1.16.0-11:/drawable-v21/...`

### drawable-xhdpi-v4.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 3.46 KB
- **Records**: 12
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/drawable-xhdpi-v4/notification_bg_normal_pressed.9.png', 'source': 'com.baseflow.geolocator.geolocator_android-core-1.16.0-11:/drawab...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 1.87 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/drawable-xxhdpi-v4/googleg_disabled_color_18.png', 'source': 'com.baseflow.geolocator.geolocator_android-play-services-base-18.3.0-13...`

### drawable.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 6.24 KB
- **Records**: 24
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/drawable/notification_tile_bg.xml', 'source': 'com.baseflow.geolocator.geolocator_android-core-1.16.0-11:/drawable/notification_tile_...`

### layout-v21.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 1.00 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/layout-v21/notification_action.xml', 'source': 'com.baseflow.geolocator.geolocator_android-core-1.16.0-11:/layout-v21/notification_ac...`

### layout.json (`flutter_valorai\build\geolocator_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 1.22 KB
- **Records**: 5
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.baseflow.geolocator.geolocator_android-release-29:/layout/notification_template_part_chronometer.xml', 'source': 'com.baseflow.geolocator.geolocator_android-core-1.16.0-11:/layout/noti...`

### navigation.json (`flutter_valorai\build\geolocator_android\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\geolocator_android\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 360.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 362.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### values-af.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-am.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 9.83 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ar.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 9.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-as.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-az.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 9.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-b+sr+Latn.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 10.00 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradl...`

### values-be.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-bg.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 9.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-bn.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-bs.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-ca.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-cs.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-da.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 9.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-de.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-el.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 9.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-en-rAU.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 5.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-en-rCA.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 5.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-en-rGB.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 9.93 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-en-rIN.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 5.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-en-rXC.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 5.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-es-rUS.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 9.94 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-es.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-et.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-eu.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-fa.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-fi.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 9.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-fr-rCA.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 9.96 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-fr.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-gl.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-gu.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 9.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-h720dp-v13.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-h720dp-v13.json`)
- **Size**: 1.40 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-h720dp-v13/values-h720dp-v13.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gra...`

### values-hdpi-v4.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hdpi-v4.json`)
- **Size**: 1.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-hdpi-v4/values-hdpi-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\...`

### values-hi.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-hr.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-hu.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-hy.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-in.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-is.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 9.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-it.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-iw.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 9.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ja.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 9.83 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ka.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-kk.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-km.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-kn.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-ko.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 9.82 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ky.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-land.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-land.json`)
- **Size**: 1.42 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-land/values-land.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cache...`

### values-large-v4.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-large-v4.json`)
- **Size**: 1.63 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-large-v4/values-large-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-ldltr-v21.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ldltr-v21.json`)
- **Size**: 1.40 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-ldltr-v21/values-ldltr-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradl...`

### values-lo.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-lt.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 9.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-lv.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 9.93 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-mk.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ml.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 9.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-mn.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-mr.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ms.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-my.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 9.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-nb.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 9.86 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ne.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 9.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-night-v8.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-night-v8.json`)
- **Size**: 1.60 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-night-v8/values-night-v8.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\...`

### values-nl.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-or.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 9.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-pa.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 9.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-pl.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-port.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-port.json`)
- **Size**: 1.36 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-port/values-port.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cache...`

### values-pt-rBR.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 9.95 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-pt-rPT.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 9.95 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### values-pt.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 5.70 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ro.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-ru.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-si.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-sk.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-sl.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-sq.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-sr.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-sv.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-sw.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-sw600dp-v13.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw600dp-v13.json`)
- **Size**: 1.62 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-sw600dp-v13/values-sw600dp-v13.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.g...`

### values-ta.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 9.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-te.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 9.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-th.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 9.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-tl.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-tr.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-uk.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-ur.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 9.89 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-uz.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-v16.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v16.json`)
- **Size**: 1.43 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-v16/values-v16.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\...`

### values-v17.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v17.json`)
- **Size**: 2.06 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-v17/values-v17.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-v18.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v18.json`)
- **Size**: 1.35 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-v18/values-v18.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-v21.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 12.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-v22.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v22.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-v22/values-v22.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-v23.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v23.json`)
- **Size**: 1.95 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-v23/values-v23.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-v24.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v24.json`)
- **Size**: 1.38 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-v24/values-v24.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-v25.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v25.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-v25/values-v25.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-v26.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v26.json`)
- **Size**: 1.61 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-v26/values-v26.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-v28.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v28.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-v28/values-v28.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tra...`

### values-vi.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-watch-v20.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-watch-v20.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-watch-v20/values-watch-v20.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradl...`

### values-watch-v21.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-watch-v21.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-watch-v21/values-watch-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-xlarge-v4.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-xlarge-v4.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/values-xlarge-v4/values-xlarge-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values-zh-rCN.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-zh-rHK.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-zh-rTW.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 9.87 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\c...`

### values-zu.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 9.88 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\...`

### values.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 96.10 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-mergeReleaseResources-34:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\...`

### anim-v21.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 292.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-fr...`

### anim.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim.json`)
- **Size**: 6.70 KB
- **Records**: 24
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/anim/abc_fade_out.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-appcompat-1.7.1-14:/anim/...`

### animator.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.56 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/animator/fragment_fade_exit.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-fragment-1.7.1-...`

### color-v23.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\color-v23.json`)
- **Size**: 2.45 KB
- **Records**: 9
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/color-v23/abc_tint_switch_track.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-appcompat-1...`

### color.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\color.json`)
- **Size**: 4.60 KB
- **Records**: 16
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/color/abc_background_cache_hint_selector_material_light.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flu...`

### drawable-hdpi-v4.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 14.12 KB
- **Records**: 46
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-hdpi-v4/abc_btn_switch_to_on_mtrl_00012.9.png', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_...`

### drawable-ldrtl-hdpi-v17.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldrtl-hdpi-v17.json`)
- **Size**: 316.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-ldrtl-hdpi-v17/abc_spinner_mtrl_am_alpha.9.png', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter...`

### drawable-ldrtl-mdpi-v17.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldrtl-mdpi-v17.json`)
- **Size**: 316.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-ldrtl-mdpi-v17/abc_spinner_mtrl_am_alpha.9.png', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter...`

### drawable-ldrtl-xhdpi-v17.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldrtl-xhdpi-v17.json`)
- **Size**: 318.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-ldrtl-xhdpi-v17/abc_spinner_mtrl_am_alpha.9.png', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutte...`

### drawable-ldrtl-xxhdpi-v17.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldrtl-xxhdpi-v17.json`)
- **Size**: 320.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-ldrtl-xxhdpi-v17/abc_spinner_mtrl_am_alpha.9.png', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutt...`

### drawable-ldrtl-xxxhdpi-v17.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldrtl-xxxhdpi-v17.json`)
- **Size**: 322.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-ldrtl-xxxhdpi-v17/abc_spinner_mtrl_am_alpha.9.png', 'source': 'io.flutter.plugins.googlemaps.google_maps_flut...`

### drawable-mdpi-v4.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 13.52 KB
- **Records**: 44
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-mdpi-v4/abc_menu_hardkey_panel_mtrl_mult.9.png', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter...`

### drawable-v21.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 1.72 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-v21/abc_list_divider_material.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-appc...`

### drawable-v23.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v23.json`)
- **Size**: 302.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-v23/abc_control_background_material.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_androi...`

### drawable-watch-v20.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-watch-v20.json`)
- **Size**: 312.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-watch-v20/abc_dialog_material_background.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_a...`

### drawable-xhdpi-v4.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 14.48 KB
- **Records**: 47
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-xhdpi-v4/abc_btn_radio_to_on_mtrl_000.png', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_andr...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 12.78 KB
- **Records**: 41
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-xxhdpi-v4/abc_tab_indicator_mtrl_alpha.9.png', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_a...`

### drawable-xxxhdpi-v4.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v4.json`)
- **Size**: 4.58 KB
- **Records**: 15
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable-xxxhdpi-v4/amu_bubble_shadow.9.png', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-and...`

### drawable.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 21.75 KB
- **Records**: 77
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/drawable/common_google_signin_btn_icon_dark_focused.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter...`

### interpolator.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\interpolator.json`)
- **Size**: 2.24 KB
- **Records**: 7
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/interpolator/btn_radio_to_on_mtrl_animation_interpolator_0.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_...`

### layout-v21.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 1.12 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/layout-v21/notification_action.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-core-1.17.0-...`

### layout-v26.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v26.json`)
- **Size**: 272.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/layout-v26/abc_screen_toolbar.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-appcompat-1.7...`

### layout-watch-v20.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-watch-v20.json`)
- **Size**: 628.00 B
- **Records**: 2
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/layout-watch-v20/abc_alert_dialog_button_bar_material.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutt...`

### layout.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 10.88 KB
- **Records**: 40
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-release-36:/layout/abc_list_menu_item_checkbox.xml', 'source': 'io.flutter.plugins.googlemaps.google_maps_flutter_android-appcompa...`

### navigation.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\google_maps_flutter_android\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\google_sign_in_android\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 362.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\google_sign_in_android\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 364.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\google_sign_in_android\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\google_sign_in_android\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### values-af.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-am.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 13.67 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-ar.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-as.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-az.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-b+sr+Latn.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 13.90 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\...`

### values-be.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-bg.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-bn.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-bs.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-ca.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-cs.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-da.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 13.71 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-de.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-el.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 13.75 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-en-rAU.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 9.60 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cach...`

### values-en-rCA.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 9.60 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\...`

### values-en-rGB.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 13.81 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cach...`

### values-en-rIN.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 9.60 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\...`

### values-en-rXC.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 9.77 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cach...`

### values-es-rUS.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 13.82 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cach...`

### values-es.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-et.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-eu.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-fa.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-fi.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-fr-rCA.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 13.84 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cach...`

### values-fr.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-gl.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-gu.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-h720dp-v13.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-h720dp-v13.json`)
- **Size**: 1.40 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-h720dp-v13/values-h720dp-v13.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\...`

### values-hdpi-v4.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hdpi-v4.json`)
- **Size**: 1.46 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-hdpi-v4/values-hdpi-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\...`

### values-hi.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-hr.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-hu.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-hy.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-in.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-is.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-it.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-iw.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 13.71 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-ja.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 13.67 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-ka.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-kk.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-km.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-kn.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-ko.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 13.66 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-ky.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-land.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-land.json`)
- **Size**: 1.41 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-land/values-land.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\...`

### values-large-v4.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-large-v4.json`)
- **Size**: 1.62 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-large-v4/values-large-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\...`

### values-ldltr-v21.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ldltr-v21.json`)
- **Size**: 1.39 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-ldltr-v21/values-ldltr-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-lo.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-lt.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-lv.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 13.77 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-mk.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-ml.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 13.75 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-mn.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-mr.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-ms.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-my.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 13.75 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-nb.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 13.71 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-ne.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-night-v8.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-night-v8.json`)
- **Size**: 1.59 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-night-v8/values-night-v8.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\...`

### values-nl.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-or.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 13.75 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-pa.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 13.71 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-pl.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-port.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-port.json`)
- **Size**: 1.35 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-port/values-port.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tran...`

### values-pt-rBR.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 13.83 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cach...`

### values-pt-rPT.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 13.83 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\...`

### values-pt.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 9.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-ro.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-ru.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-si.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-sk.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-sl.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-sq.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-sr.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-sv.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-sw.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-sw600dp-v13.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw600dp-v13.json`)
- **Size**: 1.61 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-sw600dp-v13/values-sw600dp-v13.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\...`

### values-ta.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-te.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-th.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 13.71 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-tl.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-tr.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-uk.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-ur.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 13.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-uz.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-v16.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v16.json`)
- **Size**: 1.42 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-v16/values-v16.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-v17.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v17.json`)
- **Size**: 2.06 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-v17/values-v17.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-v18.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v18.json`)
- **Size**: 1.34 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-v18/values-v18.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-v21.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 14.17 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-v22.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v22.json`)
- **Size**: 2.24 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-v22/values-v22.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-v23.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v23.json`)
- **Size**: 3.08 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-v23/values-v23.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\...`

### values-v24.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v24.json`)
- **Size**: 1.38 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-v24/values-v24.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\...`

### values-v25.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v25.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-v25/values-v25.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\...`

### values-v26.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v26.json`)
- **Size**: 2.39 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-v26/values-v26.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transf...`

### values-v28.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v28.json`)
- **Size**: 2.24 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-v28/values-v28.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\...`

### values-vi.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-watch-v20.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-watch-v20.json`)
- **Size**: 4.17 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-watch-v20/values-watch-v20.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\...`

### values-watch-v21.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-watch-v21.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-watch-v21/values-watch-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\...`

### values-xlarge-v4.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-xlarge-v4.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-xlarge-v4/values-xlarge-v4.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8....`

### values-zh-rCN.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cach...`

### values-zh-rHK.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\...`

### values-zh-rTW.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 13.72 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cach...`

### values-zu.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 13.73 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 96.86 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'io.flutter.plugins.googlesignin.google_sign_in_android-mergeReleaseResources-30:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\...`

### anim-v21.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 286.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-fragment...`

### anim.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim.json`)
- **Size**: 6.56 KB
- **Records**: 24
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/anim/abc_slide_out_top.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-appcompat-1.2.0-16:/anim/a...`

### animator.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.52 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/animator/fragment_fade_exit.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-fragment-1.7.1-1:/ani...`

### color-v23.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\color-v23.json`)
- **Size**: 2.39 KB
- **Records**: 9
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/color-v23/abc_tint_btn_checkable.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-appcompat-1.2.0-...`

### color-v26.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\color-v26.json`)
- **Size**: 270.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/color-v26/biometric_error_color.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-biometric-1.1.0-1...`

### color.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\color.json`)
- **Size**: 4.51 KB
- **Records**: 16
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/color/common_google_signin_btn_tint.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-play-services...`

### drawable-anydpi-v23.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v23.json`)
- **Size**: 300.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-anydpi-v23/fingerprint_dialog_fp_icon.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-bi...`

### drawable-anydpi-v24.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v24.json`)
- **Size**: 296.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-anydpi-v24/fingerprint_dialog_error.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-biom...`

### drawable-hdpi-v23.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v23.json`)
- **Size**: 292.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-hdpi-v23/fingerprint_dialog_error.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-biomet...`

### drawable-hdpi-v4.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 17.97 KB
- **Records**: 60
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-hdpi-v4/abc_cab_background_top_mtrl_alpha.9.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_andr...`

### drawable-ldpi-v23.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldpi-v23.json`)
- **Size**: 292.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-ldpi-v23/fingerprint_dialog_error.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-biomet...`

### drawable-ldrtl-hdpi-v17.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldrtl-hdpi-v17.json`)
- **Size**: 930.00 B
- **Records**: 3
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-ldrtl-hdpi-v17/abc_ic_menu_copy_mtrl_am_alpha.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_an...`

### drawable-ldrtl-mdpi-v17.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldrtl-mdpi-v17.json`)
- **Size**: 930.00 B
- **Records**: 3
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-ldrtl-mdpi-v17/abc_ic_menu_cut_mtrl_alpha.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_androi...`

### drawable-ldrtl-xhdpi-v17.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldrtl-xhdpi-v17.json`)
- **Size**: 936.00 B
- **Records**: 3
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-ldrtl-xhdpi-v17/abc_spinner_mtrl_am_alpha.9.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_andr...`

### drawable-ldrtl-xxhdpi-v17.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldrtl-xxhdpi-v17.json`)
- **Size**: 942.00 B
- **Records**: 3
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-ldrtl-xxhdpi-v17/abc_ic_menu_cut_mtrl_alpha.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_andr...`

### drawable-ldrtl-xxxhdpi-v17.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldrtl-xxxhdpi-v17.json`)
- **Size**: 948.00 B
- **Records**: 3
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-ldrtl-xxxhdpi-v17/abc_ic_menu_cut_mtrl_alpha.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_and...`

### drawable-mdpi-v23.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v23.json`)
- **Size**: 292.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-mdpi-v23/fingerprint_dialog_error.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-biomet...`

### drawable-mdpi-v4.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 17.38 KB
- **Records**: 58
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-mdpi-v4/abc_textfield_search_default_mtrl_alpha.9.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_i...`

### drawable-v21.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 1.69 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-v21/abc_edit_text_material.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-appcompat-1.2...`

### drawable-v23.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v23.json`)
- **Size**: 296.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-v23/abc_control_background_material.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-appc...`

### drawable-watch-v20.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-watch-v20.json`)
- **Size**: 1.28 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-watch-v20/abc_dialog_material_background.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android...`

### drawable-xhdpi-v23.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v23.json`)
- **Size**: 294.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-xhdpi-v23/fingerprint_dialog_error.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-biome...`

### drawable-xhdpi-v4.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 17.78 KB
- **Records**: 59
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-xhdpi-v4/common_google_signin_btn_text_dark_normal_background.9.png', 'source': 'io.flutter.plugins.googlesignin...`

### drawable-xxhdpi-v23.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v23.json`)
- **Size**: 296.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-xxhdpi-v23/fingerprint_dialog_error.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-biom...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 16.14 KB
- **Records**: 53
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-xxhdpi-v4/abc_ic_star_half_black_48dp.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-ap...`

### drawable-xxxhdpi-v23.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v23.json`)
- **Size**: 298.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-xxxhdpi-v23/fingerprint_dialog_error.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-bio...`

### drawable-xxxhdpi-v4.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v4.json`)
- **Size**: 7.79 KB
- **Records**: 26
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable-xxxhdpi-v4/abc_btn_radio_to_on_mtrl_000.png', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-...`

### drawable.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 19.37 KB
- **Records**: 70
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/drawable/common_google_signin_btn_text_light_focused.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_andr...`

### interpolator.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\interpolator.json`)
- **Size**: 2.20 KB
- **Records**: 7
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/interpolator/btn_checkbox_unchecked_mtrl_animation_interpolator_1.xml', 'source': 'io.flutter.plugins.googlesignin.google...`

### layout-v21.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 1.10 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/layout-v21/notification_template_icon_group.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-core-...`

### layout-v26.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v26.json`)
- **Size**: 266.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/layout-v26/abc_screen_toolbar.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-appcompat-1.2.0-16:...`

### layout-watch-v20.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-watch-v20.json`)
- **Size**: 616.00 B
- **Records**: 2
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/layout-watch-v20/abc_alert_dialog_title_material.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-...`

### layout.json (`flutter_valorai\build\google_sign_in_android\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 10.16 KB
- **Records**: 38
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'io.flutter.plugins.googlesignin.google_sign_in_android-release-32:/layout/abc_action_menu_layout.xml', 'source': 'io.flutter.plugins.googlesignin.google_sign_in_android-appcompat-1.2.0-16:...`

### navigation.json (`flutter_valorai\build\google_sign_in_android\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\google_sign_in_android\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\jni\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 355.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\jni\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 357.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\jni\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\jni\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### metadata_generation_record.json (`flutter_valorai\build\jni\intermediates\cxx\Debug\4z611j2l\logs\arm64-v8a\metadata_generation_record.json`)
- **Size**: 1.29 KB
- **Records**: 3
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 21 min SDK version: arm64-v8a', 'file_': 'C:\\Users\\mh978\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\jni-1.0.0\\src\\CMakeList...`

### metadata_generation_record.json (`flutter_valorai\build\jni\intermediates\cxx\Debug\4z611j2l\logs\armeabi-v7a\metadata_generation_record.json`)
- **Size**: 1.30 KB
- **Records**: 3
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 21 min SDK version: armeabi-v7a', 'file_': 'C:\\Users\\mh978\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\jni-1.0.0\\src\\CMakeLi...`

### metadata_generation_record.json (`flutter_valorai\build\jni\intermediates\cxx\Debug\4z611j2l\logs\x86\metadata_generation_record.json`)
- **Size**: 1.27 KB
- **Records**: 3
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 21 min SDK version: x86', 'file_': 'C:\\Users\\mh978\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\jni-1.0.0\\src\\CMakeLists.txt'...`

### metadata_generation_record.json (`flutter_valorai\build\jni\intermediates\cxx\Debug\4z611j2l\logs\x86_64\metadata_generation_record.json`)
- **Size**: 1.28 KB
- **Records**: 3
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 21 min SDK version: x86_64', 'file_': 'C:\\Users\\mh978\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\jni-1.0.0\\src\\CMakeLists.t...`

### metadata_generation_record.json (`flutter_valorai\build\jni\intermediates\cxx\RelWithDebInfo\615z6p29\logs\arm64-v8a\metadata_generation_record.json`)
- **Size**: 8.50 KB
- **Records**: 12
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 21 min SDK version: arm64-v8a', 'file_': 'C:\\Users\\mh978\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\jni-1.0.0\\src\\CMakeList...`

### metadata_generation_record.json (`flutter_valorai\build\jni\intermediates\cxx\RelWithDebInfo\615z6p29\logs\armeabi-v7a\metadata_generation_record.json`)
- **Size**: 8.56 KB
- **Records**: 12
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 21 min SDK version: armeabi-v7a', 'file_': 'C:\\Users\\mh978\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\jni-1.0.0\\src\\CMakeLi...`

### metadata_generation_record.json (`flutter_valorai\build\jni\intermediates\cxx\RelWithDebInfo\615z6p29\logs\x86\metadata_generation_record.json`)
- **Size**: 8.33 KB
- **Records**: 12
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 21 min SDK version: x86', 'file_': 'C:\\Users\\mh978\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\jni-1.0.0\\src\\CMakeLists.txt'...`

### metadata_generation_record.json (`flutter_valorai\build\jni\intermediates\cxx\RelWithDebInfo\615z6p29\logs\x86_64\metadata_generation_record.json`)
- **Size**: 8.42 KB
- **Records**: 12
- **Columns**: 9
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'level_': '0', 'message_': 'Start JSON generation. Platform version: 21 min SDK version: x86_64', 'file_': 'C:\\Users\\mh978\\AppData\\Local\\Pub\\Cache\\hosted\\pub.dev\\jni-1.0.0\\src\\CMakeLists.t...`

### values-af.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-am.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-ar.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-as.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-az.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-b+sr+Latn.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-be.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-bg.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-bn.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-bs.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-ca.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-cs.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-da.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-de.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-el.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-en-rAU.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-en-rCA.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-en-rGB.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-en-rIN.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-en-rXC.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-es-rUS.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-es.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-et.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-eu.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-fa.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-fi.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-fr-rCA.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-fr.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-gl.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-gu.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-hi.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-hr.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-hu.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-hy.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-in.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-is.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-it.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-iw.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-ja.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-ka.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-kk.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-km.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-kn.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-ko.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-ky.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-lo.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-lt.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-lv.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-mk.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-ml.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-mn.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-mr.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-ms.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-my.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-nb.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-ne.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-nl.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-or.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-pa.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-pl.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-pt-rBR.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-pt-rPT.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-pt.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-ro.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-ru.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-si.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-sk.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-sl.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-sq.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-sr.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-sv.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-sw.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-ta.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-te.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-th.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4...`

### values-tl.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-tr.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-uk.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-ur.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-uz.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-v21.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 1.68 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70...`

### values-vi.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 1.48 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values-zh-rCN.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 1.51 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-zh-rHK.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 1.51 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-zh-rTW.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 1.51 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-mergeReleaseResources-24:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-zu.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98ad81c70ba...`

### values.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 23.18 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni-release-26:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\2601acb221474fbb02680893c0c525...`

### anim-v21.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 226.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'com.github.dart_lang.jni-fragment-1.7.1-1:/anim-v21/fragment_fast_out_extra_slow_in.xml'}...`

### animator.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.17 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/animator/fragment_open_exit.xml', 'source': 'com.github.dart_lang.jni-fragment-1.7.1-1:/animator/fragment_open_exit.xml'}...`

### drawable-anydpi-v21.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v21.json`)
- **Size**: 1.28 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/drawable-anydpi-v21/ic_call_answer.xml', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/drawable-anydpi-v21/ic_call_answer.xml'}...`

### drawable-hdpi-v4.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 2.63 KB
- **Records**: 12
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/drawable-hdpi-v4/ic_call_decline.png', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/drawable-hdpi-v4/ic_call_decline.png'}...`

### drawable-ldpi-v4.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldpi-v4.json`)
- **Size**: 1.25 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/drawable-ldpi-v4/ic_call_answer_low.png', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/drawable-ldpi-v4/ic_call_answer_low.png'}...`

### drawable-mdpi-v4.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 2.39 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/drawable-mdpi-v4/ic_call_answer.png', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/drawable-mdpi-v4/ic_call_answer.png'}...`

### drawable-v21.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 230.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/drawable-v21/notification_action_background.xml', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/drawable-v21/notification_action_background.xml'}...`

### drawable-xhdpi-v4.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 2.41 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/drawable-xhdpi-v4/notification_bg_normal.9.png', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/drawable-xhdpi-v4/notification_bg_normal.9.png'}...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 1.27 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/drawable-xxhdpi-v4/ic_call_answer_video_low.png', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/drawable-xxhdpi-v4/ic_call_answer_video_low.png'}...`

### drawable-xxxhdpi-v4.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v4.json`)
- **Size**: 1.28 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/drawable-xxxhdpi-v4/ic_call_answer_low.png', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/drawable-xxxhdpi-v4/ic_call_answer_low.png'}...`

### drawable.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 806.00 B
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/drawable/notification_tile_bg.xml', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/drawable/notification_tile_bg.xml'}...`

### layout-v21.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 882.00 B
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/layout-v21/notification_template_custom_big.xml', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/layout-v21/notification_template_custom_big.xml'}...`

### layout.json (`flutter_valorai\build\jni\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 1.04 KB
- **Records**: 5
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni-release-26:/layout/notification_template_part_time.xml', 'source': 'com.github.dart_lang.jni-core-1.13.1-18:/layout/notification_template_part_time.xml'}...`

### navigation.json (`flutter_valorai\build\jni\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\jni\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\jni_flutter\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 363.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\jni_flutter\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 365.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\jni_flutter\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\jni_flutter\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### values-af.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-am.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ar.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-as.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-az.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 1.51 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-b+sr+Latn.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 1.56 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\tr...`

### values-be.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-bg.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-bn.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-bs.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ca.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-cs.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-da.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-de.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-el.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-en-rAU.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3...`

### values-en-rCA.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-en-rGB.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-en-rIN.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-en-rXC.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3...`

### values-es-rUS.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-es.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-et.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-eu.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-fa.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-fi.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-fr-rCA.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3...`

### values-fr.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-gl.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-gu.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-hi.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-hr.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-hu.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-hy.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-in.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-is.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-it.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-iw.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ja.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ka.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-kk.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-km.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-kn.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ko.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 1.49 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-ky.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-lo.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-lt.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-lv.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-mk.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ml.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 1.51 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-mn.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-mr.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ms.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-my.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 1.51 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-nb.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-ne.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-nl.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-or.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 1.51 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-pa.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-pl.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-pt-rBR.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3...`

### values-pt-rPT.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3...`

### values-pt.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ro.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-ru.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-si.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-sk.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-sl.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-sq.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-sr.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-sv.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-sw.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ta.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-te.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 1.51 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-th.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-tl.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-tr.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-uk.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-ur.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values-uz.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-v21.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 1.70 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b9...`

### values-vi.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3c4c1b98a...`

### values-zh-rCN.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 1.53 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-zh-rHK.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-release-27:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e31a86a3...`

### values-zh-rTW.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 1.52 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfor...`

### values-zu.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 1.50 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\e3...`

### values.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 23.19 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'com.github.dart_lang.jni_flutter-mergeReleaseResources-25:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\\2601acb2...`

### anim-v21.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 242.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'com.github.dart_lang.jni_flutter-fragment-1.7.1-1:/anim-v21/fragment_fast_out_extra_s...`

### animator.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.27 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/animator/fragment_open_exit.xml', 'source': 'com.github.dart_lang.jni_flutter-fragment-1.7.1-1:/animator/fragment_open_exit.xml'}...`

### drawable-anydpi-v21.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v21.json`)
- **Size**: 1.38 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/drawable-anydpi-v21/ic_call_decline_low.xml', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/drawable-anydpi-v21/ic_call_decline_l...`

### drawable-hdpi-v4.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 2.82 KB
- **Records**: 12
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/drawable-hdpi-v4/ic_call_answer.png', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/drawable-hdpi-v4/ic_call_answer.png'}...`

### drawable-ldpi-v4.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldpi-v4.json`)
- **Size**: 1.34 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/drawable-ldpi-v4/ic_call_answer.png', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/drawable-ldpi-v4/ic_call_answer.png'}...`

### drawable-mdpi-v4.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 2.56 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/drawable-mdpi-v4/notification_bg_low_pressed.9.png', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/drawable-mdpi-v4/notification_...`

### drawable-v21.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 246.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/drawable-v21/notification_action_background.xml', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/drawable-v21/notification_action_...`

### drawable-xhdpi-v4.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 2.59 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/drawable-xhdpi-v4/notification_bg_low_pressed.9.png', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/drawable-xhdpi-v4/notificatio...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 1.37 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/drawable-xxhdpi-v4/ic_call_answer.png', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/drawable-xxhdpi-v4/ic_call_answer.png'}...`

### drawable-xxxhdpi-v4.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v4.json`)
- **Size**: 1.38 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/drawable-xxxhdpi-v4/ic_call_answer_low.png', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/drawable-xxxhdpi-v4/ic_call_answer_low...`

### drawable.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 870.00 B
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/drawable/notification_bg.xml', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/drawable/notification_bg.xml'}...`

### layout-v21.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 946.00 B
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/layout-v21/notification_template_custom_big.xml', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/layout-v21/notification_template_...`

### layout.json (`flutter_valorai\build\jni_flutter\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 1.12 KB
- **Records**: 5
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'com.github.dart_lang.jni_flutter-release-27:/layout/notification_template_part_time.xml', 'source': 'com.github.dart_lang.jni_flutter-core-1.13.1-18:/layout/notification_template_part_time...`

### navigation.json (`flutter_valorai\build\jni_flutter\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\jni_flutter\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### native_assets.json (`flutter_valorai\build\native_assets\windows\native_assets.json`)
- **Size**: 45.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\package_info_plus\intermediates\aapt_friendly_merged_manifests\debug\processDebugManifest\aapt\output-metadata.json`)
- **Size**: 368.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### output-metadata.json (`flutter_valorai\build\package_info_plus\intermediates\aapt_friendly_merged_manifests\release\processReleaseManifest\aapt\output-metadata.json`)
- **Size**: 370.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\package_info_plus\intermediates\annotation_processor_list\debug\javaPreCompileDebug\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### annotationProcessors.json (`flutter_valorai\build\package_info_plus\intermediates\annotation_processor_list\release\javaPreCompileRelease\annotationProcessors.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### values-af.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-af.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-af/values-af.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-am.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-am.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-am/values-am.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-ar.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ar.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-ar/values-ar.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-as.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-as.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-as/values-as.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-az.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-az.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-az/values-az.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-b+sr+Latn.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-b+sr+Latn.json`)
- **Size**: 1.60 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-b+sr+Latn/values-b+sr+Latn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-be.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-be.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-be/values-be.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-bg.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bg.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-bg/values-bg.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-bn.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bn.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-bn/values-bn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-bs.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-bs.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-bs/values-bs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-ca.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ca.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-ca/values-ca.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-cs.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-cs.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-cs/values-cs.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-da.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-da.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-da/values-da.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-de.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-de.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-de/values-de.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-el.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-el.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-el/values-el.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-en-rAU.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rAU.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-en-rAU/values-en-rAU.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\...`

### values-en-rCA.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rCA.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-en-rCA/values-en-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cac...`

### values-en-rGB.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rGB.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-en-rGB/values-en-rGB.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\...`

### values-en-rIN.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rIN.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-en-rIN/values-en-rIN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\...`

### values-en-rXC.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-en-rXC.json`)
- **Size**: 1.60 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-en-rXC/values-en-rXC.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\...`

### values-es-rUS.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es-rUS.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-es-rUS/values-es-rUS.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\...`

### values-es.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-es.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-es/values-es.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-et.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-et.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-et/values-et.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-eu.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-eu.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-eu/values-eu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-fa.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fa.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-fa/values-fa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-fi.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fi.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-fi/values-fi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-fr-rCA.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr-rCA.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-fr-rCA/values-fr-rCA.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\...`

### values-fr.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-fr.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-fr/values-fr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-gl.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gl.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-gl/values-gl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-gu.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-gu.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-gu/values-gu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-hi.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hi.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-hi/values-hi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-hr.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hr.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-hr/values-hr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-hu.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hu.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-hu/values-hu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-hy.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-hy.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-hy/values-hy.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-in.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-in.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-in/values-in.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-is.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-is.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-is/values-is.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-it.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-it.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-it/values-it.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-iw.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-iw.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-iw/values-iw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-ja.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ja.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-ja/values-ja.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-ka.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ka.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-ka/values-ka.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-kk.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kk.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-kk/values-kk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-km.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-km.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-km/values-km.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-kn.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-kn.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-kn/values-kn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-ko.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ko.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-ko/values-ko.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-ky.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ky.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-ky/values-ky.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-lo.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lo.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-lo/values-lo.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-lt.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lt.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-lt/values-lt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-lv.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-lv.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-lv/values-lv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-mk.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mk.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-mk/values-mk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-ml.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ml.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-ml/values-ml.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-mn.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mn.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-mn/values-mn.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-mr.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-mr.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-mr/values-mr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-ms.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ms.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-ms/values-ms.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-my.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-my.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-my/values-my.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-nb.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nb.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-nb/values-nb.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-ne.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ne.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-ne/values-ne.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-nl.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-nl.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-nl/values-nl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-or.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-or.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-or/values-or.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-pa.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pa.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-pa/values-pa.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-pl.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pl.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-pl/values-pl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-pt-rBR.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rBR.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-pt-rBR/values-pt-rBR.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\...`

### values-pt-rPT.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt-rPT.json`)
- **Size**: 1.58 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-pt-rPT/values-pt-rPT.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\...`

### values-pt.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-pt.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-pt/values-pt.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-ro.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ro.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-ro/values-ro.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-ru.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ru.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-ru/values-ru.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-si.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-si.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-si/values-si.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-sk.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sk.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-sk/values-sk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-sl.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sl.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-sl/values-sl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-sq.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sq.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-sq/values-sq.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-sr.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sr.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-sr/values-sr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-sv.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sv.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-sv/values-sv.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-sw.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-sw.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-sw/values-sw.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-ta.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ta.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-ta/values-ta.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-te.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-te.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-te/values-te.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-th.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-th.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-th/values-th.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-tl.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tl.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-tl/values-tl.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-tr.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-tr.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-tr/values-tr.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-uk.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uk.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-uk/values-uk.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-ur.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-ur.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-ur/values-ur.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-uz.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-uz.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-uz/values-uz.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8...`

### values-v21.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-v21.json`)
- **Size**: 1.74 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-v21/values-v21.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\trans...`

### values-vi.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-vi.json`)
- **Size**: 1.54 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-vi/values-vi.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values-zh-rCN.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rCN.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-zh-rCN/values-zh-rCN.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cac...`

### values-zh-rHK.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rHK.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-mergeReleaseResources-24:/values-zh-rHK/values-zh-rHK.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\cac...`

### values-zh-rTW.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zh-rTW.json`)
- **Size**: 1.57 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-zh-rTW/values-zh-rTW.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\...`

### values-zu.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values-zu.json`)
- **Size**: 1.55 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values-zu/values-zu.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transfo...`

### values.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\multi-v2\values.json`)
- **Size**: 23.24 KB
- **Records**: 2
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'logs': "{'outputFile': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/values/values.xml', 'map': [{'source': 'C:\\\\Users\\\\mh978\\\\.gradle\\\\caches\\\\8.14\\\\transforms\\\...`

### anim-v21.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim-v21.json`)
- **Size**: 288.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/anim-v21/fragment_fast_out_extra_slow_in.xml', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-fragme...`

### anim.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\anim.json`)
- **Size**: 280.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/anim/fragment_fast_out_extra_slow_in.xml', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-fragment-1...`

### animator.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\animator.json`)
- **Size**: 1.54 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/animator/fragment_fade_enter.xml', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-fragment-1.7.1-1:/...`

### drawable-anydpi-v21.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-anydpi-v21.json`)
- **Size**: 1.65 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/drawable-anydpi-v21/ic_call_answer.xml', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-core-1.13.1-...`

### drawable-hdpi-v4.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-hdpi-v4.json`)
- **Size**: 3.36 KB
- **Records**: 12
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/drawable-hdpi-v4/ic_call_answer_video_low.png', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-core-...`

### drawable-ldpi-v4.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-ldpi-v4.json`)
- **Size**: 1.61 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/drawable-ldpi-v4/ic_call_answer_low.png', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-core-1.13.1...`

### drawable-mdpi-v4.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-mdpi-v4.json`)
- **Size**: 3.06 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/drawable-mdpi-v4/ic_call_answer_video.png', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-core-1.13...`

### drawable-v21.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-v21.json`)
- **Size**: 292.00 B
- **Records**: 1
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/drawable-v21/notification_action_background.xml', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-cor...`

### drawable-xhdpi-v4.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xhdpi-v4.json`)
- **Size**: 3.08 KB
- **Records**: 11
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/drawable-xhdpi-v4/ic_call_decline_low.png', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-core-1.13...`

### drawable-xxhdpi-v4.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxhdpi-v4.json`)
- **Size**: 1.63 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/drawable-xxhdpi-v4/ic_call_decline_low.png', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-core-1.1...`

### drawable-xxxhdpi-v4.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable-xxxhdpi-v4.json`)
- **Size**: 1.65 KB
- **Records**: 6
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/drawable-xxxhdpi-v4/ic_call_answer_low.png', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-core-1.1...`

### drawable.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\drawable.json`)
- **Size**: 1.03 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/drawable/notification_bg.xml', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-core-1.13.1-18:/drawab...`

### layout-v21.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout-v21.json`)
- **Size**: 1.10 KB
- **Records**: 4
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/layout-v21/notification_action_tombstone.xml', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-core-1...`

### layout.json (`flutter_valorai\build\package_info_plus\intermediates\merged_res_blame_folder\release\mergeReleaseResources\out\single\layout.json`)
- **Size**: 2.42 KB
- **Records**: 9
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'merged': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-release-26:/layout/notification_template_part_chronometer.xml', 'source': 'dev.fluttercommunity.plus.packageinfo.package_info_plus-c...`

### navigation.json (`flutter_valorai\build\package_info_plus\intermediates\navigation_json\debug\extractDeepLinksDebug\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### navigation.json (`flutter_valorai\build\package_info_plus\intermediates\navigation_json\release\extractDeepLinksRelease\navigation.json`)
- **Size**: 2.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### FontManifest.json (`flutter_valorai\build\unit_test_assets\FontManifest.json`)
- **Size**: 208.00 B
- **Records**: 2
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'family': 'MaterialIcons', 'fonts': "[{'asset': 'fonts/MaterialIcons-Regular.otf'}]"}...`

### NativeAssetsManifest.json (`flutter_valorai\build\unit_test_assets\NativeAssetsManifest.json`)
- **Size**: 45.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### Contents.json (`flutter_valorai\ios\Runner\Assets.xcassets\AppIcon.appiconset\Contents.json`)
- **Size**: 2.58 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### Contents.json (`flutter_valorai\ios\Runner\Assets.xcassets\LaunchImage.imageset\Contents.json`)
- **Size**: 414.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### Contents.json (`flutter_valorai\macos\Runner\Assets.xcassets\AppIcon.appiconset\Contents.json`)
- **Size**: 1.33 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### manifest.json (`flutter_valorai\web\manifest.json`)
- **Size**: 961.00 B
- **Records**: 4
- **Columns**: 10
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'name': 'flutter_valorai', 'short_name': 'flutter_valorai', 'start_url': '.', 'display': 'standalone', 'background_color': '#0175C2', 'theme_color': '#0175C2', 'description': 'A new Flutter project.'...`

### catboost_training.json (`pf_scraper\catboost_info\catboost_training.json`)
- **Size**: 57.60 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### all_egypt.csv (`pf_scraper\csv_output\all_egypt.csv`)
- **Size**: 45.87 MB
- **Records**: 64106
- **Columns**: 23
- **Missing %**: 10.50%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52974566', 'title': 'Luxurious Living in the Heart of Hyde Park!', 'price': '50000.0', 'currency': 'EGP', 'price_period': 'monthly', 'price_type': 'rent_price', 'price_raw_value': '50000.0', '...`

### buy.csv (`pf_scraper\csv_output\buy.csv`)
- **Size**: 14.19 MB
- **Records**: 19967
- **Columns**: 21
- **Missing %**: 0.14%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '8572018', 'title': 'SEA VIEW chalet ( 3 bedrooms ) - RTM - Foukabay', 'price': '11350000.0', 'currency': 'EGP', 'price_period': 'sell', 'price_type': 'sale_price', 'price_raw_value': '11350000...`

### commercial_buy.csv (`pf_scraper\csv_output\commercial_buy.csv`)
- **Size**: 6.22 MB
- **Records**: 8959
- **Columns**: 21
- **Missing %**: 3.43%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52713975', 'title': 'Prime Rented Retail Unit for Sale in Mirage Mall –', 'price': '7750000.0', 'currency': 'EGP', 'price_period': 'sell', 'price_type': 'sale_price', 'price_raw_value': '77500...`

### commercial_rent.csv (`pf_scraper\csv_output\commercial_rent.csv`)
- **Size**: 9.86 MB
- **Records**: 14080
- **Columns**: 21
- **Missing %**: 1.83%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52973173', 'title': 'shop rent in Fifth Settlement, Gamal Abdel Nasser', 'price': '75000', 'currency': 'EGP', 'price_period': 'monthly', 'price_type': 'rent_price', 'price_raw_value': '75000',...`

### new_projects.csv (`pf_scraper\csv_output\new_projects.csv`)
- **Size**: 1.08 MB
- **Records**: 1121
- **Columns**: 13
- **Missing %**: 30.77%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': 'b20b0954-7e37-48d3-9c99-3e13e154ad4e', 'title': 'Waterfront Residences', 'location': 'nan', 'latitude': '30.0626211', 'longitude': '30.8917422', 'images': "['https://new-projects-media.propert...`

### rent.csv (`pf_scraper\csv_output\rent.csv`)
- **Size**: 14.05 MB
- **Records**: 19979
- **Columns**: 21
- **Missing %**: 0.17%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52974566', 'title': 'Luxurious Living in the Heart of Hyde Park!', 'price': '50000', 'currency': 'EGP', 'price_period': 'monthly', 'price_type': 'rent_price', 'price_raw_value': '50000', 'prop...`

### amenity_frequency.csv (`pf_scraper\data_eg\amenity_frequency.csv`)
- **Size**: 2.21 KB
- **Records**: 60
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'amenity': 'has_amenity_ba', 'count': '18526', 'dataset': 'residential_rent'}...`

### cardinality_report.csv (`pf_scraper\data_eg\cardinality_report.csv`)
- **Size**: 1.88 KB
- **Records**: 60
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'feature': 'id', 'unique_values': '19914', 'dataset': 'residential_rent'}...`

### commercial_rent.parquet (`pf_scraper\data_eg\commercial_rent.parquet`)
- **Size**: 946.62 KB
- **Records**: 12377
- **Columns**: 73
- **Missing %**: 16.98%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52973173', 'title': 'shop rent in Fifth Settlement, Gamal Abdel Nasser', 'price': '75000.0', 'currency': 'EGP', 'price_period': 'monthly', 'price_type': 'rent_price', 'price_raw_value': '75000...`

### commercial_sale.parquet (`pf_scraper\data_eg\commercial_sale.parquet`)
- **Size**: 754.69 KB
- **Records**: 8469
- **Columns**: 69
- **Missing %**: 18.40%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52713975', 'title': 'Prime Rented Retail Unit for Sale in Mirage Mall –', 'price': '7750000.0', 'currency': 'EGP', 'price_period': 'sell', 'price_type': 'sale_price', 'price_raw_value': '77500...`

### compound_frequency.csv (`pf_scraper\data_eg\compound_frequency.csv`)
- **Size**: 11.36 KB
- **Records**: 375
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'compound_name': 'The City', 'count': '13014', 'dataset': 'residential_rent'}...`

### coordinate_quality_report.csv (`pf_scraper\data_eg\coordinate_quality_report.csv`)
- **Size**: 210.00 B
- **Records**: 6
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'geo_validation_status': 'valid', 'count': '19914', 'dataset': 'residential_rent'}...`

### dataset_stats.json (`pf_scraper\data_eg\dataset_stats.json`)
- **Size**: 7.27 KB
- **Records**: 4
- **Columns**: 4
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'residential_rent': '19914', 'residential_sale': '19880', 'commercial_rent': '12313', 'commercial_sale': '8448'}...`

### feature_registry.csv (`pf_scraper\data_eg\feature_registry.csv`)
- **Size**: 5.67 KB
- **Records**: 77
- **Columns**: 6
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'feature_name': 'id', 'source': 'raw', 'datatype': 'object', 'nullable': 'False', 'description': 'Feature id from raw', 'category': 'raw'}...`

### missing_values_report.csv (`pf_scraper\data_eg\missing_values_report.csv`)
- **Size**: 12.93 KB
- **Records**: 296
- **Columns**: 5
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'feature': 'id', 'missing_count': '0', 'dataset': 'residential_rent', 'total_rows': '19914', 'missing_percentage': '0.0'}...`

### phase3_results.json (`pf_scraper\data_eg\phase3_results.json`)
- **Size**: 20.11 KB
- **Records**: 8
- **Columns**: 5
- **Missing %**: 50.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'residential_rent': "{'total_rows': 19914, 'features': 58}", 'valerti_edge_case': 'nan', 'residential_sale': "{'total_rows': 19880, 'features': 58}", 'commercial_rent': "{'total_rows': 12377, 'featur...`

### residential_rent.parquet (`pf_scraper\data_eg\residential_rent.parquet`)
- **Size**: 1.30 MB
- **Records**: 19914
- **Columns**: 77
- **Missing %**: 15.63%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52974566', 'title': 'Luxurious Living in the Heart of Hyde Park!', 'price': '50000.0', 'currency': 'EGP', 'price_period': 'monthly', 'price_type': 'rent_price', 'price_raw_value': '50000.0', '...`

### residential_sale.parquet (`pf_scraper\data_eg\residential_sale.parquet`)
- **Size**: 1.59 MB
- **Records**: 19880
- **Columns**: 77
- **Missing %**: 15.62%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '8572018', 'title': 'SEA VIEW chalet ( 3 bedrooms ) - RTM - Foukabay', 'price': '11350000.0', 'currency': 'EGP', 'price_period': 'sell', 'price_type': 'sale_price', 'price_raw_value': '11350000...`

### text_feature_dictionary.json (`pf_scraper\data_eg\text_feature_dictionary.json`)
- **Size**: 1.23 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### text_feature_frequency.csv (`pf_scraper\data_eg\text_feature_frequency.csv`)
- **Size**: 2.76 KB
- **Records**: 84
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'text_feature': 'is_furnished', 'count': '7628', 'dataset': 'residential_rent'}...`

### catboost_training.json (`pf_scraper\data_eg\catboost_info\catboost_training.json`)
- **Size**: 55.14 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### hybrid_dataset_report.json (`pf_scraper\data_eg\dataset_hybrid_v1\hybrid_dataset_report.json`)
- **Size**: 1.13 KB
- **Records**: 5
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'residential_rent.parquet': '8846', 'residential_sale.parquet': '13655'}...`

### residential_rent.parquet (`pf_scraper\data_eg\dataset_hybrid_v1\residential_rent.parquet`)
- **Size**: 883.51 KB
- **Records**: 8846
- **Columns**: 83
- **Missing %**: 8.53%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52974566', 'title': 'Luxurious Living in the Heart of Hyde Park!', 'price': '50000.0', 'currency': 'EGP', 'price_period': 'monthly', 'price_type': 'rent_price', 'price_raw_value': '50000.0', '...`

### residential_sale.parquet (`pf_scraper\data_eg\dataset_hybrid_v1\residential_sale.parquet`)
- **Size**: 1.41 MB
- **Records**: 13655
- **Columns**: 83
- **Missing %**: 11.27%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52973883', 'title': 'Pool View Studio in noor city,Near Best way', 'price': '1850000.0', 'currency': 'EGP', 'price_period': 'sell', 'price_type': 'sale_price', 'price_raw_value': '1850000.0', ...`

### amenity_frequency.csv (`pf_scraper\data_eg\dataset_v2\amenity_frequency.csv`)
- **Size**: 2.14 KB
- **Records**: 58
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'amenity': 'has_amenity_ba', 'count': '18326', 'dataset': 'residential_rent'}...`

### cardinality_report.csv (`pf_scraper\data_eg\dataset_v2\cardinality_report.csv`)
- **Size**: 1.90 KB
- **Records**: 60
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'feature': 'id', 'unique_values': '19701', 'dataset': 'residential_rent'}...`

### commercial_rent.parquet (`pf_scraper\data_eg\dataset_v2\commercial_rent.parquet`)
- **Size**: 898.57 KB
- **Records**: 11344
- **Columns**: 71
- **Missing %**: 14.66%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52448220', 'title': 'Clubhouse (Gym-Cafe) for rent in Joya Compound', 'price': '450000.0', 'currency': 'EGP', 'price_period': 'monthly', 'price_type': 'rent_price', 'price_raw_value': '450000....`

### commercial_sale.parquet (`pf_scraper\data_eg\dataset_v2\commercial_sale.parquet`)
- **Size**: 750.74 KB
- **Records**: 8090
- **Columns**: 69
- **Missing %**: 15.51%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '8680642', 'title': 'Pharmacy for Sale Prime Location Acacia Mall', 'price': '33670000.0', 'currency': 'EGP', 'price_period': 'sell', 'price_type': 'sale_price', 'price_raw_value': '33670000.0'...`

### compound_frequency.csv (`pf_scraper\data_eg\dataset_v2\compound_frequency.csv`)
- **Size**: 10.77 KB
- **Records**: 342
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'compound_name': 'The City', 'count': '13943', 'dataset': 'residential_rent'}...`

### coordinate_quality_report.csv (`pf_scraper\data_eg\dataset_v2\coordinate_quality_report.csv`)
- **Size**: 210.00 B
- **Records**: 6
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'geo_validation_status': 'valid', 'count': '19701', 'dataset': 'residential_rent'}...`

### feature_registry.csv (`pf_scraper\data_eg\dataset_v2\feature_registry.csv`)
- **Size**: 5.67 KB
- **Records**: 77
- **Columns**: 6
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'feature_name': 'id', 'source': 'raw', 'datatype': 'object', 'nullable': 'False', 'description': 'Feature id from raw', 'category': 'raw'}...`

### missing_values_report.csv (`pf_scraper\data_eg\dataset_v2\missing_values_report.csv`)
- **Size**: 12.86 KB
- **Records**: 294
- **Columns**: 5
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'feature': 'id', 'missing_count': '0', 'dataset': 'residential_rent', 'total_rows': '19701', 'missing_percentage': '0.0'}...`

### phase3_5_results.json (`pf_scraper\data_eg\dataset_v2\phase3_5_results.json`)
- **Size**: 20.35 KB
- **Records**: 8
- **Columns**: 5
- **Missing %**: 50.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'residential_rent': "{'total_rows': 13606, 'features': 58}", 'valerti_edge_case': 'nan', 'residential_sale': "{'total_rows': 18076, 'features': 58}", 'commercial_rent': "{'total_rows': 9844, 'feature...`

### residential_rent.parquet (`pf_scraper\data_eg\dataset_v2\residential_rent.parquet`)
- **Size**: 1.31 MB
- **Records**: 19701
- **Columns**: 77
- **Missing %**: 13.03%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52974566', 'title': 'Luxurious Living in the Heart of Hyde Park!', 'price': '50000.0', 'currency': 'EGP', 'price_period': 'monthly', 'price_type': 'rent_price', 'price_raw_value': '50000.0', '...`

### residential_sale.parquet (`pf_scraper\data_eg\dataset_v2\residential_sale.parquet`)
- **Size**: 1.61 MB
- **Records**: 19617
- **Columns**: 77
- **Missing %**: 13.03%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '8698066', 'title': 'Ready to move garden apt 140 sqm , 8 years plan.', 'price': '800000.0', 'currency': 'EGP', 'price_period': 'sell', 'price_type': 'sale_price', 'price_raw_value': '800000.0'...`

### text_feature_dictionary.json (`pf_scraper\data_eg\dataset_v2\text_feature_dictionary.json`)
- **Size**: 1.31 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### text_feature_frequency.csv (`pf_scraper\data_eg\dataset_v2\text_feature_frequency.csv`)
- **Size**: 2.76 KB
- **Records**: 84
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'text_feature': 'is_furnished', 'count': '7515', 'dataset': 'residential_rent'}...`

### amenity_frequency.csv (`pf_scraper\data_eg\dataset_v3\amenity_frequency.csv`)
- **Size**: 2.13 KB
- **Records**: 58
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'amenity': 'has_amenity_ba', 'count': '8139', 'dataset': 'residential_rent'}...`

### cardinality_report.csv (`pf_scraper\data_eg\dataset_v3\cardinality_report.csv`)
- **Size**: 1.75 KB
- **Records**: 56
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'feature': 'id', 'unique_values': '8846', 'dataset': 'residential_rent'}...`

### commercial_rent.parquet (`pf_scraper\data_eg\dataset_v3\commercial_rent.parquet`)
- **Size**: 740.44 KB
- **Records**: 8546
- **Columns**: 71
- **Missing %**: 14.75%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52448220', 'title': 'Clubhouse (Gym-Cafe) for rent in Joya Compound', 'price': '450000.0', 'currency': 'EGP', 'price_period': 'monthly', 'price_type': 'rent_price', 'price_raw_value': '450000....`

### commercial_rent_schema.json (`pf_scraper\data_eg\dataset_v3\commercial_rent_schema.json`)
- **Size**: 914.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### commercial_sale.parquet (`pf_scraper\data_eg\dataset_v3\commercial_sale.parquet`)
- **Size**: 662.51 KB
- **Records**: 6691
- **Columns**: 69
- **Missing %**: 15.52%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '8680642', 'title': 'Pharmacy for Sale Prime Location Acacia Mall', 'price': '33670000.0', 'currency': 'EGP', 'price_period': 'sell', 'price_type': 'sale_price', 'price_raw_value': '33670000.0'...`

### commercial_sale_schema.json (`pf_scraper\data_eg\dataset_v3\commercial_sale_schema.json`)
- **Size**: 878.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### compound_frequency.csv (`pf_scraper\data_eg\dataset_v3\compound_frequency.csv`)
- **Size**: 10.73 KB
- **Records**: 341
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'compound_name': 'The City', 'count': '6094', 'dataset': 'residential_rent'}...`

### coordinate_quality_report.csv (`pf_scraper\data_eg\dataset_v3\coordinate_quality_report.csv`)
- **Size**: 208.00 B
- **Records**: 6
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'geo_validation_status': 'valid', 'count': '8846', 'dataset': 'residential_rent'}...`

### dedup_stats.json (`pf_scraper\data_eg\dataset_v3\dedup_stats.json`)
- **Size**: 751.00 B
- **Records**: 5
- **Columns**: 4
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'residential_rent': '19979.0', 'residential_sale': '19966.0', 'commercial_rent': '14080.0', 'commercial_sale': '8959.0'}...`

### feature_registry.csv (`pf_scraper\data_eg\dataset_v3\feature_registry.csv`)
- **Size**: 5.69 KB
- **Records**: 77
- **Columns**: 6
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'feature_name': 'id', 'source': 'raw', 'datatype': 'object', 'nullable': 'False', 'description': 'Feature id from raw', 'category': 'raw'}...`

### missing_values_report.csv (`pf_scraper\data_eg\dataset_v3\missing_values_report.csv`)
- **Size**: 12.70 KB
- **Records**: 294
- **Columns**: 5
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'feature': 'id', 'missing_count': '0', 'dataset': 'residential_rent', 'total_rows': '8846', 'missing_percentage': '0.0'}...`

### phase3_6_results.json (`pf_scraper\data_eg\dataset_v3\phase3_6_results.json`)
- **Size**: 19.52 KB
- **Records**: 8
- **Columns**: 5
- **Missing %**: 50.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'residential_rent': "{'total_rows': 8846, 'features': 57}", 'valerti_edge_case': 'nan', 'residential_sale': "{'total_rows': 13655, 'features': 57}", 'commercial_rent': "{'total_rows': 8546, 'features...`

### residential_rent.parquet (`pf_scraper\data_eg\dataset_v3\residential_rent.parquet`)
- **Size**: 716.05 KB
- **Records**: 8846
- **Columns**: 77
- **Missing %**: 13.04%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52974566', 'title': 'Luxurious Living in the Heart of Hyde Park!', 'price': '50000.0', 'currency': 'EGP', 'price_period': 'monthly', 'price_type': 'rent_price', 'price_raw_value': '50000.0', '...`

### residential_rent_schema.json (`pf_scraper\data_eg\dataset_v3\residential_rent_schema.json`)
- **Size**: 1022.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### residential_sale.parquet (`pf_scraper\data_eg\dataset_v3\residential_sale.parquet`)
- **Size**: 1.19 MB
- **Records**: 13655
- **Columns**: 77
- **Missing %**: 13.02%
- **Duplicates %**: 0.0
- **Example Row**: `{'id': '52973883', 'title': 'Pool View Studio in noor city,Near Best way', 'price': '1850000.0', 'currency': 'EGP', 'price_period': 'sell', 'price_type': 'sale_price', 'price_raw_value': '1850000.0', ...`

### residential_sale_schema.json (`pf_scraper\data_eg\dataset_v3\residential_sale_schema.json`)
- **Size**: 1022.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### text_feature_dictionary.json (`pf_scraper\data_eg\dataset_v3\text_feature_dictionary.json`)
- **Size**: 1.31 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### text_feature_frequency.csv (`pf_scraper\data_eg\dataset_v3\text_feature_frequency.csv`)
- **Size**: 2.75 KB
- **Records**: 84
- **Columns**: 3
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'text_feature': 'is_furnished', 'count': '3168', 'dataset': 'residential_rent'}...`

### hybrid_training_results.json (`pf_scraper\data_eg\models_hybrid_v1\hybrid_training_results.json`)
- **Size**: 900.00 B
- **Records**: 3
- **Columns**: 2
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'Rent': "{'MAPE': 0.359984799054096, 'MAE': 24835.483827493263, 'RMSE': 52437.17454667066, 'R2': 0.237060030690658}", 'Sale': "{'MAPE': 0.378479547143766, 'MAE': 3965157.735403727, 'RMSE': 6879339.88...`

### exposure_registry.json (`pf_scraper\fair-price-eg\backend\app\geo\exposure_registry.json`)
- **Size**: 30.58 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### residential_rent_schema.json (`pf_scraper\fair-price-eg\backend\app\models\residential_rent_schema.json`)
- **Size**: 1022.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### residential_sale_schema.json (`pf_scraper\fair-price-eg\backend\app\models\residential_sale_schema.json`)
- **Size**: 1022.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### buy_clean.csv (`pf_scraper\fair-price-eg\data\buy_clean.csv`)
- **Size**: 4.73 MB
- **Records**: 19915
- **Columns**: 14
- **Missing %**: 0.09%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '8572018', 'category': 'buy', 'price_egp': '11350000.0', 'period': 'sale', 'property_type': 'Chalet', 'bedrooms': '3.0', 'bathrooms': '2.0', 'size_sqm': '129.0', 'location_text': 'Fouka...`

### commercial_buy_clean.csv (`pf_scraper\fair-price-eg\data\commercial_buy_clean.csv`)
- **Size**: 1.82 MB
- **Records**: 8776
- **Columns**: 14
- **Missing %**: 5.07%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52713975', 'category': 'commercial_buy', 'price_egp': '7750000.0', 'period': 'sale', 'property_type': 'Retail', 'bedrooms': 'nan', 'bathrooms': '1.0', 'size_sqm': '45.0', 'location_tex...`

### commercial_rent_clean.csv (`pf_scraper\fair-price-eg\data\commercial_rent_clean.csv`)
- **Size**: 2.99 MB
- **Records**: 13938
- **Columns**: 14
- **Missing %**: 2.72%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52973173', 'category': 'commercial_rent', 'price_egp': '75000.0', 'period': 'monthly', 'property_type': 'Shop', 'bedrooms': 'nan', 'bathrooms': '1.0', 'size_sqm': '52.0', 'location_tex...`

### rent_residential.csv (`pf_scraper\fair-price-eg\data\rent_residential.csv`)
- **Size**: 4.63 MB
- **Records**: 19979
- **Columns**: 14
- **Missing %**: 0.04%
- **Duplicates %**: 0.0
- **Example Row**: `{'listing_id': '52974566', 'category': 'rent', 'price_egp': '50000.0', 'period': 'monthly', 'property_type': 'Apartment', 'bedrooms': '3.0', 'bathrooms': '3', 'size_sqm': '189.0', 'location_text': 'Hy...`

### areas.csv (`pf_scraper\fair-price-eg\db\seed\areas.csv`)
- **Size**: 0.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### area_aliases.csv (`pf_scraper\fair-price-eg\db\seed\area_aliases.csv`)
- **Size**: 0.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### listings_rent_residential.csv (`pf_scraper\fair-price-eg\db\seed\listings_rent_residential.csv`)
- **Size**: 0.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### metadata.json (`pf_scraper\fair-price-eg\frontend\metadata.json`)
- **Size**: 139.00 B
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### package-lock.json (`pf_scraper\fair-price-eg\frontend\package-lock.json`)
- **Size**: 189.46 KB
- **Records**: 393
- **Columns**: 5
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'name': 'valorai-frontend', 'version': '0.0.0', 'lockfileVersion': '3', 'requires': 'True', 'packages': "{'name': 'valorai-frontend', 'version': '0.0.0', 'dependencies': {'@tailwindcss/vite': '^4.1.1...`

### package.json (`pf_scraper\fair-price-eg\frontend\package.json`)
- **Size**: 1.27 KB
- **Records**: 33
- **Columns**: 7
- **Missing %**: 28.14%
- **Duplicates %**: 3.0303030303030303
- **Example Row**: `{'name': 'valorai-frontend', 'private': 'True', 'version': '0.0.0', 'type': 'module', 'scripts': 'vite --port=3000 --host=0.0.0.0', 'dependencies': 'nan', 'devDependencies': 'nan'}...`

### tsconfig.json (`pf_scraper\fair-price-eg\frontend\tsconfig.json`)
- **Size**: 606.00 B
- **Records**: 15
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 33.33333333333333
- **Example Row**: `{'compilerOptions': 'ES2022'}...`

### package-lock.json (`pf_scraper\fair-price-eg\frontend old\package-lock.json`)
- **Size**: 637.17 KB
- **Records**: 1315
- **Columns**: 5
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'name': 'frontend', 'version': '0.1.0', 'lockfileVersion': '3', 'requires': 'True', 'packages': "{'name': 'frontend', 'version': '0.1.0', 'dependencies': {'@testing-library/dom': '^10.4.1', '@testing...`

### package.json (`pf_scraper\fair-price-eg\frontend old\package.json`)
- **Size**: 849.00 B
- **Records**: 15
- **Columns**: 7
- **Missing %**: 42.86%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'name': 'frontend', 'version': '0.1.0', 'private': 'True', 'dependencies': '^10.4.1', 'scripts': 'nan', 'eslintConfig': 'nan', 'browserslist': 'nan'}...`

### manifest.json (`pf_scraper\fair-price-eg\frontend old\public\manifest.json`)
- **Size**: 492.00 B
- **Records**: 3
- **Columns**: 7
- **Missing %**: 0.00%
- **Duplicates %**: Error calculating (complex types)
- **Example Row**: `{'short_name': 'React App', 'name': 'Create React App Sample', 'icons': "{'src': 'favicon.ico', 'sizes': '64x64 32x32 24x24 16x16', 'type': 'image/x-icon'}", 'start_url': '.', 'display': 'standalone',...`

### egypt_villas_3br_2bath.csv (`pf_scraper\kaggle_eg\egypt_villas_3br_2bath.csv`)
- **Size**: 539.30 KB
- **Records**: 291
- **Columns**: 38
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'amenities': '["BA", "CP", "PG", "SP", "ST", "VW", "SE", "SS", "SY", "WC", "BL"]', 'amenity_count': '11', 'amenity_names': '["Balcony", "Covered Parking", "Private Garden", "Shared Pool", "Study", "V...`

### dubai_commercial_buy.csv (`pf_scraper\kaggle_uae\dubai_commercial_buy.csv`)
- **Size**: 110.46 KB
- **Records**: 175
- **Columns**: 24
- **Missing %**: 13.48%
- **Duplicates %**: 0.0
- **Example Row**: `{'amenities': 'nan', 'amenity_count': '0', 'bathrooms': 'nan', 'bedrooms': 'nan', 'category': 'commercial_buy', 'currency': 'AED', 'has_coordinates': 'True', 'id': '51191461', 'images': '["https://sta...`

### dubai_commercial_rent.csv (`pf_scraper\kaggle_uae\dubai_commercial_rent.csv`)
- **Size**: 112.67 KB
- **Records**: 175
- **Columns**: 24
- **Missing %**: 12.79%
- **Duplicates %**: 0.0
- **Example Row**: `{'amenities': 'nan', 'amenity_count': '0', 'bathrooms': 'nan', 'bedrooms': 'nan', 'category': 'commercial_rent', 'currency': 'AED', 'has_coordinates': 'True', 'id': '51611110', 'images': '["https://st...`

### dubai_new_projects.csv (`pf_scraper\kaggle_uae\dubai_new_projects.csv`)
- **Size**: 213.17 KB
- **Records**: 168
- **Columns**: 15
- **Missing %**: 6.67%
- **Duplicates %**: 0.0
- **Example Row**: `{'amenity_count': '0', 'category': 'new_projects', 'has_coordinates': 'True', 'id': '313d42a8-67e4-43fd-9331-4414a2bdabd6', 'images': '["https://new-projects-media.propertyfinder.com/project/313d42a8-...`

### dubai_residential_buy.csv (`pf_scraper\kaggle_uae\dubai_residential_buy.csv`)
- **Size**: 1.12 MB
- **Records**: 1548
- **Columns**: 24
- **Missing %**: 0.44%
- **Duplicates %**: 0.0
- **Example Row**: `{'amenities': '["CP", "SE", "BA", "BL", "LB", "BK", "SY", "SP", "CS", "BW"]', 'amenity_count': '10', 'bathrooms': '3', 'bedrooms': '2.0', 'category': 'buy', 'currency': 'AED', 'has_coordinates': 'True...`

### dubai_residential_rent.csv (`pf_scraper\kaggle_uae\dubai_residential_rent.csv`)
- **Size**: 14.72 MB
- **Records**: 20051
- **Columns**: 24
- **Missing %**: 0.46%
- **Duplicates %**: 0.0
- **Example Row**: `{'amenities': '["BA", "BW", "AC"]', 'amenity_count': '3', 'bathrooms': '3.0', 'bedrooms': '3.0', 'category': 'rent', 'currency': 'AED', 'has_coordinates': 'True', 'id': '16295055', 'images': '["https:...`

### next_data_eg_only.json (`pf_scraper\provider\next_data_eg_only.json`)
- **Size**: 358.19 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

### metadata.json (`react valorai\metadata.json`)
- **Size**: 214.00 B
- **Records**: 1
- **Columns**: 4
- **Missing %**: 0.00%
- **Duplicates %**: 0.0
- **Example Row**: `{'name': 'ValorAI', 'description': 'AI-Powered Real Estate Intelligence Platform', 'requestFramePermissions': 'camera', 'majorCapabilities': 'MAJOR_CAPABILITY_SERVER_SIDE_GEMINI_API'}...`

### package.json (`react valorai\package.json`)
- **Size**: 845.00 B
- **Records**: 22
- **Columns**: 7
- **Missing %**: 27.92%
- **Duplicates %**: 4.545454545454546
- **Example Row**: `{'name': 'react-example', 'private': 'True', 'version': '0.0.0', 'type': 'module', 'scripts': 'vite --port=3000 --host=0.0.0.0', 'dependencies': 'nan', 'devDependencies': 'nan'}...`

### tsconfig.json (`react valorai\tsconfig.json`)
- **Size**: 508.00 B
- **Records**: 14
- **Columns**: 1
- **Missing %**: 0.00%
- **Duplicates %**: 35.714285714285715
- **Example Row**: `{'compilerOptions': 'ES2022'}...`

### catboost_training.json (`scripts\catboost_info\catboost_training.json`)
- **Size**: 9.47 KB
- **Records**: 0
- **Columns**: 0
- **Missing %**: 0.00%
- **Duplicates %**: 0

