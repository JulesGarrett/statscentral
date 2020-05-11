from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
# from cities.models import Cities, Reviews
from cities.models import CityReviews
from cities.forms import CreateReviewForm, UpdateReviewForm
from account.models import Account


######################################
#         Helper Functions           #
######################################

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# old function that was used in old deliverable
def get_cities_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT City, Sum(Population) AS Population FROM `cities_cities` group by City Limit 10;")
        cities = dictfetchall(cursor)
    return cities

# query that is used to search for cities by name
def search_city_match(query=None):
    with connection.cursor() as cursor:
        cursor.execute("SELECT City_ID as CityID, City, State FROM C_US_MilitaryCities WHERE City LIKE '%" + str(query)+ "%' Order by length(City), City, State Limit 25")
        cities = dictfetchall(cursor)
    return cities

# need to change to be large query with tons of joins
def get_city_by_id(id=None):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM C_US_MilitaryCities WHERE CITY_ID = "+str(id))
        city = dictfetchall(cursor)
    return city[0]

# pulls just city id and population
def get_population_by_id(id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT City_ID, SUM(Population) AS Pop FROM C_ZipCodeFix WHERE CITY_ID = "+str(id)+" GROUP BY City_ID")
            id_pop = dictfetchall(cursor)
        if len(id_pop) > 0:
            return id_pop[0]
        else: return {"City_ID":id, "Pop":" No Population Data Found"}

def get_top_7_state_tax(cityid):
        with connection.cursor() as cursor:
            cursor.execute("select us.State as state, st.Tax_Type as tax, st.AMOUNT/1000000 as amount from C_UnitedStates as us, C_StateTax st, C_US_MilitaryCities as mil_c where mil_c.City_ID = "+str(cityid)+" and mil_c.State_ID = us.State_ID and us.State = st.State and st.Tax_Type <> 'Total Taxes' group by us.State, st.Tax_Type, st.AMOUNT order by amount desc limit 7")
            st_tax = dictfetchall(cursor)
        return st_tax

def get_state_tax(cityid):
        with connection.cursor() as cursor:
            cursor.execute('''select * from
                                (select us.State as state, st.Tax_Type as tax, st.AMOUNT as amount
                                    from C_UnitedStates as us, C_StateTax st, C_US_MilitaryCities as mil_c
                                    where mil_c.City_ID = '''+str(cityid)+''' and mil_c.State_ID = us.State_ID
                                    and us.State = st.State and st.Tax_Type <> 'Total Taxes'
                                    group by us.State, st.Tax_Type, st.AMOUNT order by st.Tax_Type) a
                                left join (select st.Tax_Type as tax, avg(st.AMOUNT) as avg_amount
                                    from C_StateTax st
                                    where st.State <> 'Total_US'
                                    group by st.Tax_Type order by st.Tax_Type) b
                                on a.tax = b.tax
                                order by avg_amount''')
            st_tax_avg = dictfetchall(cursor)
        return st_tax_avg

def get_reviews_by_city(cityid):
    with connection.cursor() as cursor:
        cursor.execute("select mcs.City, mcs.State, cr.Rating, cr.Comments from (Select mc.City, us.State from (select State_ID, City from C_US_MilitaryCities where City_ID = "+str(cityid)+") mc left join C_UnitedStates us on us.State_ID = mc.State_ID) mcs left join cities_cityreviews cr on mcs.City = cr.City and mcs.State = cr.State")
        reviews = dictfetchall(cursor)
    return reviews

def get_cityavg_ratings_by_city(cityid):
    with connection.cursor() as cursor:
        cursor.execute("select mcs.City, mcs.State, avg(cr.Rating) as avg_rating from (Select mc.City, us.State from (select State_ID, City from C_US_MilitaryCities where City_ID = "+str(cityid)+") mc left join C_UnitedStates us on us.State_ID = mc.State_ID) mcs left join cities_cityreviews cr on mcs.City = cr.City and mcs.State = cr.State")
        rating = dictfetchall(cursor)
    return rating[0]

def get_stateavg_ratings_by_city(cityid):
    with connection.cursor() as cursor:
        cursor.execute("select mcs.State, avg(cr.Rating) as avg_rating from (Select us.State from (select State_ID from C_US_MilitaryCities where City_ID = "+str(cityid)+") mc left join C_UnitedStates us on us.State_ID = mc.State_ID) mcs left join cities_cityreviews cr on mcs.State = cr.State group by mcs.State")
        rating = dictfetchall(cursor)
    return rating[0]

def get_militarybases(cityid):
        with connection.cursor() as cursor:
            cursor.execute('''select cs.State, mb.SiteName, mb.Component, mb.Status from M_MilitaryBases mb
                                right join (select us.State from C_US_MilitaryCities mc
                                	           left join C_UnitedStates us on us.State_ID = mc.State_ID
                                	           where mc.City_ID = '''+str(cityid)+''') cs on cs.State = mb.State order by Status ASC''')
            bases = dictfetchall(cursor)
        return bases

def get_militarycare(cityid):
        with connection.cursor() as cursor:
            cursor.execute('''Select cf.FacilityName, cf.PRIM_SVC, cf.S_CITY, cf.S_STATE, cf.S_ADD1, cf.S_ADD2, cf.Type from M_Polytrauma_Care_Facility cf
                                right join (select City, State from C_US_MilitaryCities mc
                                where mc.City_ID = '''+str(cityid)+''') cs on cs.State = cf.S_STATE''')
            care_centers = dictfetchall(cursor)
        return care_centers

def get_militarygrantsavg(cityid):
        with connection.cursor() as cursor:
            cursor.execute('''select g.GrantValue, a.g_avg from M_VA_HomeGrant g, (SELECT avg(GrantValue) as g_avg from M_VA_HomeGrant) a
                                where g.State = (select mc.State from C_US_MilitaryCities mc
                                					where mc.City_ID = '''+str(cityid)+''')''')
            avgs = dictfetchall(cursor)
        return avgs

def get_military_grant_per_population(cityid):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT hg.State, hg.GrantValue/pop.Pop as val_per_person,
                                 CASE When hg.State = (select State from C_US_MilitaryCities where City_ID = '''+str(cityid)+''')
                                     THEN "#e85d47" ELSE "#17a2b8" END AS color
                                 From M_VA_HomeGrant hg
                                 left join (SELECT us.ST_Code, p.Pop
                                     from C_UnitedStates us left join (select State_ID, SUM(Population) as Pop
                                                                         from C_ZipCodeFix group by State_ID) p
                                                              on p.State_ID = us.State_ID) pop
                                  on pop.ST_Code = hg.State order by val_per_person desc''')
            ratios = dictfetchall(cursor)
        return ratios

def get_bully_avg():
        with connection.cursor() as cursor:
            cursor.execute('''select avg(BiasOfSexAllegations) as sex_al,
                                avg(Sex_race_Origin_Allegations) as sex_race_al, avg(BiasOfDisabilityAllegations) as dis_al
                                from S_Bullying_HarrassmentReports''')
            avgs = dictfetchall(cursor)
        return avgs

def get_bully_data(cityid):
        with connection.cursor() as cursor:
            cursor.execute('''select st.State, BiasOfSexAllegations as sex_al, Sex_race_Origin_Allegations as sex_race_al, BiasOfDisabilityAllegations as dis_al
                                 from S_Bullying_HarrassmentReports bhs
                                 right join (select State from C_UnitedStates
                                             where State_ID = (select State_ID from C_US_MilitaryCities where City_ID = '''+str(cityid)+''')) st
                                 on st.State = bhs.State''')
            state_vals = dictfetchall(cursor)
            avgs = get_bully_avg()
        return {"avgs":avgs[0], "state_vals":state_vals[0]}

def get_bully_data_by_state(cityid):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT bhr.State, bhr.NumOfSchools as schools, bhr.NumAllegations/bhr.NumOfSchools as al_per_school,
                                 CASE When bhr.State = (select State from C_UnitedStates us
                                                          right join (select State_ID from C_US_MilitaryCities where City_ID = '''+str(cityid)+''') st
                                                          on st.State_ID = us.State_ID)
                                  THEN "#20c8e3" ELSE "#17a2b8" END AS color From S_Bullying_HarrassmentReports bhr
                                  order by State asc''')
            values = dictfetchall(cursor)
        return values

def get_teach_data_by_state(cityid):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT tce.State, tce.FullTimeTeachers/tce.NumOfSchools as teach_per_school, tce.Cert_Lic_Percent,
                                     CASE When tce.State = (select State from C_UnitedStates us
                                                             right join (select State_ID from C_US_MilitaryCities where City_ID = '''+str(cityid)+''') st
                                                             on st.State_ID = us.State_ID)
                                     THEN "#20c8e3" ELSE "#17a2b8" END AS color
                                     From S_SCH_TeacherCertAndExperience tce
                                     order by State asc''')
            values = dictfetchall(cursor)
        return values

def get_sales_tax_by_state(cityid):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT tx.State, tx.CombinedRate,
                                    CASE When tx.State = (select State from C_UnitedStates us
                                                            right join (select State_ID from C_US_MilitaryCities where City_ID = '''+str(cityid)+''') st
                                                            on st.State_ID = us.State_ID)
                                    THEN "#e85d47" ELSE "#17a2b8" END AS color From C_StateTaxPercent tx order by State asc''')
            values = dictfetchall(cursor)
        return values

def city_match_query(max_pop, min_pop, mil, base):
    # just pop
    if mil =="No" and base == "No":
        with connection.cursor() as cursor:
            cursor.execute('''Select mc.State as StateCode, mc.City, z.City_Id as CityID, z.total_pop from
                            (Select City_ID, Sum(Population) as total_pop from C_ZipCodeFix
                            group by City_ID
                            having total_pop >= '''+str(min_pop)+''' and total_pop <= '''+str(max_pop)+''') z
                            left join C_US_MilitaryCities mc on mc.City_ID = z.City_ID limit 100''')
            cities = dictfetchall(cursor)
    # pop plus bool mil aid
    elif mil !="No" and base == "No":
        with connection.cursor() as cursor:
            cursor.execute('''select * from (
                                Select us.State as State, mc.State as StateCode, mc.City, z.City_Id as CityID, z.total_pop
                                    from (Select City_ID, Sum(Population) as total_pop from C_ZipCodeFix
                                                group by City_ID
                                                having total_pop >= '''+str(min_pop)+''' and total_pop <= '''+str(max_pop)+''') z
                                                left join C_US_MilitaryCities mc on mc.City_ID = z.City_ID
                                                left join C_UnitedStates us on us.State_ID = mc.State_ID) base
                                    where City in (SELECT S_CITY from M_Polytrauma_Care_Facility)''')
            cities = dictfetchall(cursor)
    # pop plus base type
    elif mil =="No" and base != "No":
        with connection.cursor() as cursor:
            cursor.execute('''select * from (
                                Select us.State, mc.City, z.City_Id as CityID, z.total_pop
                                    from (Select City_ID, Sum(Population) as total_pop from C_ZipCodeFix
                                                group by City_ID
                                                having total_pop >= '''+str(min_pop)+''' and total_pop <= '''+str(max_pop)+''') z
                                                left join C_US_MilitaryCities mc on mc.City_ID = z.City_ID
                                                left join C_UnitedStates us on us.State_ID = mc.State_ID) base
                                    where State in (SELECT State from M_MilitaryBases where Component = "'''+str(base)+'''") limit 100''')
            cities = dictfetchall(cursor)
    # everything
    else:
        with connection.cursor() as cursor:
            cursor.execute('''select * from (
                                Select us.State as State, mc.State as StateCode, mc.City, z.City_Id as CityID, z.total_pop
                                    from (Select City_ID, Sum(Population) as total_pop from C_ZipCodeFix
                                                group by City_ID
                                                having total_pop >= '''+str(min_pop)+''' and total_pop <= '''+str(max_pop)+''') z
                                                left join C_US_MilitaryCities mc on mc.City_ID = z.City_ID
                                                left join C_UnitedStates us on us.State_ID = mc.State_ID) base
                                    where State in (SELECT State from M_MilitaryBases where Component = "'''+str(base)+'''")
                                    and City in (SELECT S_CITY from M_Polytrauma_Care_Facility)''')
            cities = dictfetchall(cursor)
    if len(cities) > 0:
        return cities
    else: return {"City":"No Cities found with those requirements"}

######################################
#          View Functions            #
######################################

def home_screen_view(request):
    context = {}
    return render(request, "cities/home.html", context)


def search_cities(request):
    context = {}
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)
        context['cities'] = search_city_match(query)
    return render(request, 'cities/search.html', context)


def city_match(request):
    context = {}
    if request.GET:
        max_pop = request.GET['max_pop']
        min_pop = request.GET['min_pop']
        mil = request.GET['military']
        base = request.GET['m_base']
        context['min_pop'] = int(min_pop)
        context['max_pop'] = int(max_pop)
        context['m_base'] = str(base)
        context['military'] = str(mil)
        context['cities'] = city_match_query(max_pop, min_pop, mil, base)
    return render(request, "cities/city_match.html", context)


def detail_city(request, id):
    context = {}
    city = get_city_by_id(id)
    cityid_pop = get_population_by_id(id)
    context['city'] = city
    context['cityid_pop'] = cityid_pop
    context['st_tax'] = get_top_7_state_tax(id)
    context['st_tax_avg'] = get_state_tax(id)
    context['reviews'] = get_reviews_by_city(id)
    context['city_rating'] = get_cityavg_ratings_by_city(id)
    context['state_rating'] = get_stateavg_ratings_by_city(id)
    context['militarybases'] = get_militarybases(id)
    context['militarycare'] = get_militarycare(id)
    context['military_grantavgs'] = get_militarygrantsavg(id)
    context['grant_per_pop'] = get_military_grant_per_population(id)
    context['school_bully'] = get_bully_data(id)
    context['school_bully_st'] = get_bully_data_by_state(id)
    context['school_teacher'] = get_teach_data_by_state(id)
    context['sales_tax'] = get_sales_tax_by_state(id)
    return render(request, 'cities/city_detail.html', context)


############### REVIEW ###############
def create_review(request):
    context = {}
    user = request.user
    if request.POST:
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            author = Account.objects.filter(email=request.user.email).first()
            obj.author = author
            obj.save()
    else:
        form = CreateReviewForm()
    context['form'] = form
    return render(request, 'cities/create_review.html', context)


def detail_review(request, slug):
    context = {}
    review = get_object_or_404(CityReviews, slug=slug)
    context['review'] = review
    return render(request, 'cities/detail_review.html', context)


def delete_review(request, slug):
    context = {}
    obj = get_object_or_404(CityReviews, slug=slug)
    context['object'] = obj
    if request.POST:
        obj.delete()
        return redirect('home')
    return render(request, "cities/delete_review.html", context)


def edit_review(request, slug):
    context = {}
    user = request.user

    review = get_object_or_404(CityReviews, slug=slug)
    if request.POST:
        form = UpdateReviewForm(request.POST or None, instance=review)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated Review for "+str(review.City)
            review = obj

    form = UpdateReviewForm(
			initial={
					"Comments": review.Comments,
					"Rating": review.Rating,
				}
			)
    context['form'] = form
    context['city'] = review.City
    return render(request, 'cities/edit_review.html', context)
