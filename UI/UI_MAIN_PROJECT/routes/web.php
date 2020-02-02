<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/


Route::get('/','SqlController@index');

Route::get('/initial/{value}', 'SqlController@showInitial')->name('initial');

Route::get('/context/{MASSECHET_NAME}/{DAF_NAME}/{AMUD_NAME}/{ROW_ID}')->name('Massechet');

// Dynamic table

Route::get('/initial_list_dynamic','SqlController@initials_list');
Route::get('/context/{MASSECHET_NAME}/{DAF_NAME}/{AMUD_NAME}/{ROW_ID}','SqlController@getContext')->name('Massechet');
