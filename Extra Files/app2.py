# from flask import Flask, render_template
# from flask import Flask, render_template, redirect, url_for, request
# import new_app

# app = Flask(__name__)

# # Route for the homepage
# @app.route('/')
# def homepage():
#     return render_template('layout.html')

# # Route for Feature Wise Selection
# @app.route('/feature_wise_selection')
# def feature_wise_selection():
#     # return render_template('new.html')
#     return render_template('new.html', company_names=get_unique_companyname_names(), price_ranges=get_price_ranges(),
#                            cameras=get_unique_cam(), displays=get_unique_disp(), rating_ranges=get_rating_ranges())

#     # return redirect(url_for('new_index'))
#     #  return redirect(url_for('feature_wise_selection'))

# # Route for Compare Two Mobile
# @app.route('/compare_two_mobile')
# def compare_two_mobile():
#     return redirect(url_for('compare_two_mobile'))
#     # return render_template('index2.html')

# # Route for Mobile Review
# @app.route('/mobile_review')
# def mobile_review():
#     return render_template('index.html')

# # Route for Chart
# @app.route('/chart')
# def chart():
#     return render_template('chart.html')

# if __name__ == '__main__':
#     app.run(debug=True)
